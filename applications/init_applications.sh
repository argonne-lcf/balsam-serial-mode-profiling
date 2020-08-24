#!/bin/bash

APP_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

echo $APP_DIR

balsam app --name cosmics_gen_stage --exec "$APP_DIR/cosmics_gen_stage.sh" --postprocess "${APP_DIR}/parse_log_times.py"

balsam app --name array_add --exec "$APP_DIR/array_add.py" --postprocess "${APP_DIR}/parse_log_times.py"

balsam app --name empty_app --exec "$APP_DIR/empty_app.sh" --postprocess "${APP_DIR}/parse_log_times.py"
