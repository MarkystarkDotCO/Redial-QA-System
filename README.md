<!-- activate venv -->
source myenv/bin/activate

<!-- start  jupyter-->
jupyter notebook

<!-- start  mlflow-->
mlflow ui

<!--  Serving docker  -->
mlflow models build-docker --model-uri f"models:/Iris_rf/3"  --name "random_forest_model_v0.01 "

<!-- Serving locally -->
curl https://pyenv.run | bash
python -m  pip install virtualenv
PATH="$HOME/.pyenv/bin:$PATH"
export MLFLOW_TRACKING_URI=http://127.0.0.1:5000
mlflow models serve -m runs:/efdc0254e1584d27ad1e5572b978dc3e/explainer -p 8080

<!-- expose prometheus -->
chmod +w  /Users/methanolkaeokrachang/Documents/myapp/spark/metrics
mlflow server --host 0.0.0.0 --port 5001 --expose-prometheus /Users/methanolkaeokrachang/Documents/myapp/spark/metrics

<!-- super user -->
sudo su

