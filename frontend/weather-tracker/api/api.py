from flask import Flask, request
import polars as pl

app = Flask(__name__)


@app.route("/check", methods=['GET'])
def check_if_country_valid() -> bool:
    countries_df = pl.read_csv('./countries.csv')
    args = request.args.to_dict()
    country = args.get("country")

    for df_country in countries_df['name']:
        if country.title() == df_country:
            return {'found': True}

    return {'found': False, 'country': country}
