from flask import Flask, render_template, flash
from config import Config
from forms import CalcForm
from calc import pois_metric, bern_metric, reynolds_num, bern_max_metric
from decimal import Decimal

app = Flask(__name__)
app.config.from_object(Config)


@app.route('/', methods=['GET', 'POST'])
def calc():
    form = CalcForm()

    if form.validate_on_submit():

        pipe_diameter_metric = 0.0254 * float(form.pipe_diameter_field.data)
        pipe_length_metric = 0.3048 * float(form.pipe_length_field.data)
        delta_p_metric = 6894.76 * float(form.delta_p_field.data)

        flow_rate_lam_imp = None
        flow_rate_turb_imp = None
        flow_rate_max_imp = None
        reynolds_number = None

        try:
            flow_rate_max_metric = bern_max_metric(pipe_diameter_metric, delta_p_metric)
            flow_rate_max_imp = "%.2f" % Decimal(flow_rate_max_metric * 15850.3)
        except ValueError:
            flash("There was a math value error. Check your numbers and try again.")
        except TypeError:
            flash("There was a type error. Make sure you are entering numbers without units and try again.")

        try:
            flow_rate_lam_metric = pois_metric(pipe_diameter_metric, delta_p_metric, pipe_length_metric)
            flow_rate_lam_imp = "%.2f" % Decimal(flow_rate_lam_metric * 15850.3)

        except ValueError:
            flash("There was a math value error. Check your numbers and try again.")
        except TypeError:
            flash("There was a type error. Make sure you are entering numbers without units and try again.")

        try:
            flow_rate_turb_metric = bern_metric(pipe_diameter_metric, delta_p_metric, pipe_length_metric)[0]
            flow_rate_turb_imp = "%.2f" % Decimal(flow_rate_turb_metric * 15850.3)
            # velocity_metric = bern_metric(pipe_diameter_metric, delta_p_metric, pipe_length_metric)[1]
            # velocity_imp = "%.2f" % Decimal(velocity_metric * 3.28084)

        except ValueError:
            flash("There was a math value error. Check your numbers and try again.")
        except TypeError:
            flash("There was a type error. Make sure you are entering numbers without units and try again.")

        try:
            reynolds_number = "%.2E" % Decimal(reynolds_num(pipe_diameter_metric, delta_p_metric, pipe_length_metric))
        except ValueError:
            flash("There was a math value error. Check your numbers and try again.")
        except TypeError:
            flash("There was a type error. Make sure you are entering numbers without units and try again.")

        return render_template('index.html', title='Water Flow Calculator', form=form, execute=True,
                               q_lam_imp=flow_rate_lam_imp, q_turb_imp=flow_rate_turb_imp,
                               r_num=reynolds_number, q_max_imp=flow_rate_max_imp)
    return render_template('index.html', title='Flowrate Calculator', form=form, execute=False)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
