from flask import Flask, request, render_template, url_for
import base64
from gradient_generator import gradient_generator as gen
from playlist_data import playlist_data as pd

playlist_error = "Unable to retrieve playlist data."

app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/playlist_img", methods=["POST"])
def display_image():
    if request.method == "POST":

        # ======================
        # RETRIEVE PLAYLIST DATA
        # ======================

        playlist_link = request.form.get("playlist_url")
        metadata, tracks = pd.get_playlist_data(playlist_link)
        if(metadata == None or tracks == None or tracks == []):
            return render_template("index.html", playlist_error=playlist_error)

        # =======================
        # RETRIEVE ATTRIBUTE DATA
        # =======================

        attribute_data = pd.get_attr_data(tracks)
        average_data = pd.get_avg_attr_data(attribute_data)

        # ==================
        # GENERATE GRADIENTS
        # ==================

        img1_data = gen.gen_linear_vert_grad_from_attr(average_data["tempo"], average_data["valence"], average_data["energy"], average_data["acousticness"]).getvalue()
        img1_base64 = base64.b64encode(img1_data).decode("utf-8")

        img2_data = gen.gen_linear_diamond_grad_from_attr(average_data["tempo"], average_data["valence"], average_data["energy"], average_data["acousticness"]).getvalue()
        img2_base64 = base64.b64encode(img2_data).decode("utf-8")

        img3_data = gen.gen_linear_radial_grad_from_attr(average_data["tempo"], average_data["valence"], average_data["energy"], average_data["acousticness"]).getvalue()
        img3_base64 = base64.b64encode(img3_data).decode("utf-8")

        # ======
        # RENDER
        # ======
        
        return render_template("index.html", metadata=metadata, attribute_data=average_data, img1=img1_base64, img2=img2_base64, img3=img3_base64)