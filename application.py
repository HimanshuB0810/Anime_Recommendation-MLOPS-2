from flask import render_template,request,Flask
from pipeline.predication_pipeline import hybrid_recommendation
import traceback

app=Flask(__name__)

@app.route('/',methods=['GET','POST'])
def home():
    recommendations=None

    if request.method=='POST':
        try:
            # user_id_raw = request.form["userID"]
            # user_id=int(user_id_raw) if user_id_raw and user_id_raw.strip() else None

            selected_genre = request.form.getlist("genres")
            genre_list = selected_genre if selected_genre else []


            recommendations=hybrid_recommendation(genre_list=genre_list)
        except Exception as e:
            print("Error Ocuured")
            traceback.print_exc()

    return render_template('index.html',recommendations=recommendations)

if __name__=="__main__":
    app.run(debug=True,host='0.0.0.0',port=7860)