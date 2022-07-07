import pandas as pd
import gspread
from difflib import get_close_matches

def main(query):

    sa = gspread.service_account(filename="service_account.json")
    sh = sa.open("database")
    wks = sh.worksheet("database")

    df_wks = pd.DataFrame(wks.get_all_records())

    try:
        df = df_wks[df_wks['Common Name'].str.lower() == query.lower()]
        index_specie_num = int(str(df.index).replace("Int64Index([", "").replace("], dtype='int64')", ""))
        # name
        common_name = str(df.at[index_specie_num, "Common Name"])
        scientific_name = str(df.at[index_specie_num, "Scientific Name"])
        # taxonomy
        organism_type = str(df.at[index_specie_num, "Organism Type"])
        order = str(df.at[index_specie_num, "Order"])
        family = str(df.at[index_specie_num, "Family"])
        genus = str(df.at[index_specie_num, "Genus"])
        # habitat
        habitat_range = str(df.at[index_specie_num, "Range"])
        habitat = str(df.at[index_specie_num, "Habitat"])
        # lifespan
        average_lifespan = str(df.at[index_specie_num, "Average Lifespan"])
        # food
        eating_habit = str(df.at[index_specie_num, "Eating Habits"])
        appetite = str(df.at[index_specie_num, "Appetite"])
        # media
        image_url = str(df.at[index_specie_num, "Image"])
        video_url = str(df.at[index_specie_num, "Video"])
        audio_url = str(df.at[index_specie_num, "Audio"])
        # size
        height = str(df.at[index_specie_num, "Height (in cm)"])
        width = str(df.at[index_specie_num, "Width (in cm)"])
        length = str(df.at[index_specie_num, "Length (in cm)"])
        # weight
        weight = str(df.at[index_specie_num, "Weight"])
        #Credit
        image_credit = str(df.at[index_specie_num, "Image Credit"])
        video_credit = str(df.at[index_specie_num, "Video Credit"])
        audio_credit = str(df.at[index_specie_num, "Audio Credit"])

        image_url = str(image_url.replace("https://drive.google.com/open?id=", "https://drive.google.com/uc?export=view&id="))
        video_url = str(video_url.replace("https://drive.google.com/open?id=","https://drive.google.com/file/d/") + "/preview")
        audio_url = str(audio_url.replace("https://drive.google.com/open?id=", "https://docs.google.com/uc?export=download&id="))



        HTML = (
            "<html>"
            "<head>"
            "<meta charset=\"utf-8\">"
            "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">"
            "<link rel=\"icon\" type=\"image/x-icon\" href=\"" + image_url + "\" >"
            "<title>" + common_name + " | Living Taxonomy" + "</title>"
            "</head>"

            "<h1><u>" + common_name + "</u></h1>"

            "<img src=\"" + image_url + "\"alt=\"" + common_name + "\"style=\"width: 100%; height: auto\"<br>"
            "<p>Image by: " + image_credit + "</p>"

            "<br>"
            "<br>"

            "<iframe src=\"" + video_url + "\"allowfullscreen=\"true\" style=\"width: auto; height: auto\"></iframe>"
            "<p>Video by: " + video_credit + "</p>"

            "<br>"
            "<br>"

            "<audio controls> <source src=\"" + audio_url + "\"> </audio>"
            "<p>Audio by: " + audio_credit + "</p>"

            "<h3><u> Name </u></h3>"
            "<p><b>Common Name:</b> " + common_name + "</p>"
            "<p><b>Scientific Name:</b> " + scientific_name + "</p>"

            "<br>"

            "<p><b>Organism Type:</b> " + organism_type + "</p>"

            "<br>"

            "<h3><u> Size </u></h3>"
            "<p><b>Width(in cm):</b> " + width + "</p>"
            "<p><b>Length(in cm):</b> " + length + "</p>"
            "<p><b>Height(in cm):</b> " + height + "</p>"
            "<p><b>Weight:</b> " + weight + "</p>"

            "<br>"

            "<h3><u> Taxonomy </u></h3>"
            "<p><b>Order: </b>" + order + "</p>"
            "<p><b>Family: </b>" + family + "</p>"
            "<p><b>Genus: </b>" + genus + "</p>"

            "<br>"

            "<h3><u>Habitat</u></h3>"
            "<p><b>Range:</b> " + habitat_range + "</p>"
            "<p><b>Habitat:</b> " + habitat + "</p>"

            "<br>"

            "<p><b>Average Lifespan:</b> " + average_lifespan + "<p>"

            "<br>"

            "<h3><u> Food Consumption </u></h3>"
            "<p><b>Eating Habits:</b> " + eating_habit + "</p>"
            "<p><b>Appetite:</b> " + appetite + "</p>"

            "</html>"
        )

        return(str(HTML))

    except ValueError:
        close_matches = get_close_matches(query.lower(), df_wks['Common Name'].tolist())

        suggestStr = "" 
        for x in close_matches:
            suggestStr = suggestStr + "<a href=\"/?query=" + x.replace(" ", "+") + "\">" + x + "</a><br>"
        
        if suggestStr == "":
            return(open("static/404.html").read())
        else:
            suggestStr = "<html><head><meta name=\"viewport\" content=\"width = device-width, initial-scale = 1.0\"><link rel=\"icon\" type=\"image/x-icon\" href=\"https://raw.githubusercontent.com/Living-Taxonomy/Living-Taxonomy-Website-Media/main/Logo.png\"></head><body><h1> Nearest Match(s) </h1>" + suggestStr + "</body></html>"
            return(suggestStr)
