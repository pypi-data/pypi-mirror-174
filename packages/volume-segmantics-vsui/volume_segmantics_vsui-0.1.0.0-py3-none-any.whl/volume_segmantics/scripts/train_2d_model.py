#!/usr/bin/env python

import logging
import sys
from datetime import date
from pathlib import Path
import vsui_client.vsui_client as vsui_client
import atexit
sys.path.insert(0, '/dls/science/users/jig77871/projects/volume-segmantics')

import volume_segmantics.utilities.config as cfg
from volume_segmantics.data import (TrainingDataSlicer, get_settings_data)
from volume_segmantics.model import VolSeg2dTrainer
from volume_segmantics.utilities import get_2d_training_parser
def exit_handler():
    vsui_client.disconnect()

atexit.register(exit_handler)

def main():
    logger = logging.getLogger()
    handler = vsui_client.RequestHandler()
    logging.basicConfig(
        level=logging.INFO, format=cfg.LOGGING_FMT, datefmt=cfg.LOGGING_DATE_FMT
    )
    logger.addHandler(handler)
    # Parse args and check correct number of volumes given
    parser = get_2d_training_parser()
    args = parser.parse_args()
    data_vols = getattr(args, cfg.TRAIN_DATA_ARG)
    label_vols = getattr(args, cfg.LABEL_DATA_ARG)

    # connect to vsui server if it is enabled
    vsui_id = getattr(args, cfg.VSUI_PROCESS_ID_ARG)
    if vsui_id != "vsui_disabled":
        vsui_client.set_task_id(vsui_id)
        vsui_client.set_logging_target('Logs')
        vsui_client.connect()

    root_path = Path(getattr(args, cfg.DATA_DIR_ARG)).resolve()
    logging.info(f'root_path: {root_path}')

    # Create the settings object
    settings_path = Path(root_path, cfg.SETTINGS_DIR, cfg.TRAIN_SETTINGS_FN)
    settings = get_settings_data(settings_path)

    if len(data_vols) != len(label_vols):
        logging.error(
            "Number of data volumes and number of label volumes must be equal!"
        )
        print(f'data vols:{data_vols}')
        print(f'label vols:{label_vols}')
        sys.exit(1)

    data_im_out_dir = root_path / settings.data_im_dirname  # dir for data imgs
    seg_im_out_dir = root_path / settings.seg_im_out_dirname  # dir for seg imgs
    # Keep track of the number of labels
    max_label_no = 0
    label_codes = None
    # Set up the DataSlicer and slice the data volumes into image files
    for count, (data_vol_path, label_vol_path) in enumerate(zip(data_vols, label_vols)):
        slicer = TrainingDataSlicer(data_vol_path, label_vol_path, settings)
        data_prefix, label_prefix = f"data{count}", f"seg{count}"
        slicer.output_data_slices(data_im_out_dir, data_prefix)
        slicer.output_label_slices(seg_im_out_dir, label_prefix)
        if slicer.num_seg_classes > max_label_no:
            max_label_no = slicer.num_seg_classes
            label_codes = slicer.codes
    assert label_codes is not None
    # Set up the 2dTrainer
    trainer = VolSeg2dTrainer(data_im_out_dir, seg_im_out_dir, max_label_no, settings)
    # Train the model, first frozen, then unfrozen
    num_cyc_frozen = settings.num_cyc_frozen
    num_cyc_unfrozen = settings.num_cyc_unfrozen
    model_type = settings.model["type"].name
    model_fn = f"{date.today()}_{model_type}_{settings.model_output_fn}.pytorch"
    model_out = Path(root_path, model_fn)
    trainer.output_comparison_figures()
    vsui_client.notify('training started', 'info')
    if num_cyc_frozen > 0:
        trainer.train_model(
            model_out, num_cyc_frozen, settings.patience, create=True, frozen=True
        )
    if num_cyc_unfrozen > 0 and num_cyc_frozen > 0:
        trainer.train_model(
            model_out, num_cyc_unfrozen, settings.patience, create=False, frozen=False
        )
    elif num_cyc_unfrozen > 0 and num_cyc_frozen == 0:
        trainer.train_model(
            model_out, num_cyc_unfrozen, settings.patience, create=True, frozen=False
        )
    trainer.output_loss_fig(model_out)
    trainer.output_prediction_figure(model_out)
    # Clean up all the saved slices
    slicer.clean_up_slices()
    vsui_client.deactivate_task()
    vsui_client.notify('training completed', 'success')
    vsui_client.disconnect()


if __name__ == "__main__":
    main()
