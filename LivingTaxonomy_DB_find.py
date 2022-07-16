import pandas as pd
import gspread
from difflib import get_close_matches
import random

def main(query):
    sa = gspread.service_account(filename="service_account.json")
    sh = sa.open("database")
    wks = sh.worksheet("database")
    df_wks = pd.DataFrame(wks.get_all_records())

    if query:
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



            HTML = (open("static/specie_page.html").read()
            #Image
            .replace("image_url", image_url)
            .replace("image_credit", image_credit)
            #Video
            .replace("video_url", video_url)
            .replace("video_credit", video_credit)
            #Audio
            .replace("audio_url", audio_url)
            .replace("audio_credit", audio_credit)
            #Name
            .replace("common_name", common_name)
            .replace("scientific_name", scientific_name)
            #Organism type
            .replace("organism_type", organism_type)
            #Size
            .replace("width_cm", width)
            .replace("length_cm", length)
            .replace("height_cm", height)
            .replace("weight_x", weight)
            #Taxonomy
            .replace("order_x", order)
            .replace("family_x", family)
            .replace("genus_x", genus)
            #Habitat
            .replace("habitat_range", habitat_range)
            .replace("habitat_x", habitat)
            #Average Lifespan
            .replace("average_lifespan", average_lifespan)
            #Food Consumption
            .replace("eating_habit", eating_habit)
            .replace("appetite", appetite)
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
                return(open("static/suggest_search.html").read()
                .replace("suggestStr", suggestStr)
                .replace("search_query", query)
                )
    else:
        randnum = random.randint(2, wks.row_count)

        return(open("static/index.html").read()
        #Background
        .replace("randombg", df_wks.at[randnum, "Image"])
        .replace("https://drive.google.com/open?id=", "http://drive.google.com/uc?export=view&id=")
        #More Info
        .replace("randomspecie", "/?query=" + df_wks.at[randnum, "Common Name"].replace(" ", "+") + "")
        )
