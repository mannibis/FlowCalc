from flask import Flask, render_template, flash, redirect, url_for
from config import Config
from forms import CalcForm
from calc import pois_metric
from calc import bern_metric
from calc import reynolds_num
from decimal import Decimal

app = Flask(__name__)
app.config.from_object(Config)


@app.route('/calc', methods=['GET', 'POST'])
def calc():
    form = CalcForm()

    if form.validate_on_submit():

        pipe_diameter_metric = 0.0254 * float(form.pipe_diameter_field.data)
        pipe_length_metric = 0.3048 * float(form.pipe_length_field.data)
        delta_p_metric = 6894.76 * float(form.delta_p_field.data)

        flow_rate_lam_imp = None
        flow_rate_turb_imp = None
        velocity_imp = None
        reynolds_number = None

        try:
            flow_rate_lam_metric = pois_metric(pipe_diameter_metric, delta_p_metric, pipe_length_metric)
            flow_rate_lam_imp = "%.2f" % Decimal(flow_rate_lam_metric * 15850.3)

            # flash("Q (laminar) = %.2f gpm" % Decimal(flow_rate_lam_imp))
        except ValueError:
            flash("There was a math value error. Check your numbers and try again.")
        except TypeError:
            flash("There was a type error. Make sure you are entering numbers without units and try again.")

        try:
            flow_rate_turb_metric = bern_metric(pipe_diameter_metric, delta_p_metric, pipe_length_metric)[0]
            velocity_metric = bern_metric(pipe_diameter_metric, delta_p_metric, pipe_length_metric)[1]
            flow_rate_turb_imp = "%.2f" % Decimal(flow_rate_turb_metric * 15850.3)
            velocity_imp = "%.2f" % Decimal(velocity_metric * 3.28084)

            # flash("Q (turbulent) = %.2f gpm" % Decimal(flow_rate_turb_imp))
            # flash("V (turbulent) = %.2f ft/s" % Decimal(velocity_imp))
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

        return render_template('index.html', title='Calculate Flowrate', form=form, execute=True,
                               q_lam_imp=flow_rate_lam_imp, q_turb_imp=flow_rate_turb_imp, v_turb_imp=velocity_imp,
                               r_num=reynolds_number)
    return render_template('index.html', title='Calculate Flowrate', form=form, execute=False)


if __name__ == '__main__':
    app.run(debug=True, port=5000)
