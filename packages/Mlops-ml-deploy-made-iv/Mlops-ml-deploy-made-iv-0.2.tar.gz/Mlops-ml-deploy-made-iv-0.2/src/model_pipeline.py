import json
import logging
from pathlib import Path, PurePath

import click
import pandas as pd

from src.data import read_csv, split_train_val_data
from src.entities import TotalPipelineParams, read_training_pipeline_params
from src.features import preprocessing_pipeline, extract_target
from src.models import (train_model, predict_model, load_model, save_model, evaluate_model)

logging.basicConfig(
    filename=PurePath(Path(__file__).parents[0], Path(f'logs/{__name__}.log')),
    format='%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
    datefmt='%Y-%m-%d:%H:%M:%S',
    level=logging.DEBUG,
    filemode='a')
logger = logging.getLogger(__name__)


def run_pipeline(config_path: str, process_type: str) -> None:
    params = read_training_pipeline_params(config_path)
    df = read_csv(params.dataset_params.input_file_path)

    train_df, val_df = split_train_val_data(df, params.splitting_params, params.dataset_params)

    train_df, train_target = extract_target(train_df, params.feature_params)
    val_df, val_target = extract_target(val_df, params.feature_params)

    preprocess = preprocessing_pipeline(params.preprocessing_params)
    if process_type == 'train':
        train_df = pd.DataFrame(preprocess.fit_transform(train_df))
        model = train_model(train_df, train_target, params.model_params)
        save_model(model, params.model_params)
    if process_type == 'predict':
        val_df = pd.DataFrame(preprocess.fit_transform(val_df))
        model = load_model(params.model_params)
        predicted_val_target = predict_model(model, val_df)
        results = evaluate_model(predicted_val_target, val_target)
        json.dump()


@click.command(name="pipeline")
@click.option('--process-type', type=click.Choice(['train', 'predict'], case_sensitive=False))
@click.argument("config_path")
def model_pipeline(process_type: str, config_path: str):
    run_pipeline(config_path, process_type)


if __name__ == "__main__":
    model_pipeline()
