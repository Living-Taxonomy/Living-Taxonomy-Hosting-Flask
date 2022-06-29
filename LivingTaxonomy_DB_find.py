import pandas as pd
import gspread

def main(query):

    sa = gspread.service_account(filename="service_account.json")
    sh = sa.open("database")
    wks = sh.worksheet("database")

    df_wks = pd.DataFrame(wks.get_all_records())

        
    # More precessing on server; case un-sensetive
    df = df_wks[df_wks['Common Name'].str.lower() == query.lower().replace("-", " ")]
    index_specie_num = int(str(df.index).replace("Int64Index([", "").replace("], dtype='int64')", ""))

    #name
    common_name = df.at[index_specie_num, "Common Name"]
    scientific_name = df.at[index_specie_num, "Scientific Name"]
    #taxonomy
    order = df.at[index_specie_num, "Order"]
    organism_type = df.at[index_specie_num, "Organism Type"]
    family = df.at[index_specie_num, "Family"]
    genus = df.at[index_specie_num, "Genus"]
    #habitat
    habitat_range = df.at[index_specie_num, "Range"]
    habitat = df.at[index_specie_num, "Habitat"]
    #lifespan
    average_lifespan = df.at[index_specie_num, "Average Lifespan"]
    #food
    eating_habit = df.at[index_specie_num, "Eating Habits"]
    appetite = df.at[index_specie_num, "Appetite"]
    #media
    image_url = df.at[index_specie_num, "Image"]
    video_url = df.at[index_specie_num, "Video"]
    audio_url = df.at[index_specie_num, "Audio"]
    #size
    height = df.at[index_specie_num, "Height (in cm)"]
    width = df.at[index_specie_num, "Width (in cm)"]
    length = df.at[index_specie_num, "Length (in cm)"]
    #weight
    weight = df.at[index_specie_num, "Weight"]

    image_url = image_url.replace("https://drive.google.com/open?id=", "https://drive.google.com/uc?export=view&id=")
    video_url = str(video_url.replace("https://drive.google.com/open?id=", "https://drive.google.com/file/d/") + "/preview")
    audio_url = audio_url.replace("https://drive.google.com/open?id=", "https://docs.google.com/uc?export=download&id=")

    """
    # More api calls; case sensitive
    specie_cell_row = wks.find(query)

    common_name = df.at[specie_cell_row.row-2, "Common Name"]
    scientific_name = df.at[specie_cell_row.row-2, "Scientific Name"]
    organism_type = df.at[specie_cell_row.row-2, "Organism Type"]
    family = df.at[specie_cell_row.row-2, "Family"]
    genus = df.at[specie_cell_row.row-2, "Genus"]
    habitat = df.at[specie_cell_row.row-2, "Habitat"]
    average_lifespan = df.at[specie_cell_row.row-2, "Average Lifespan"]
    eating_habit = df.at[specie_cell_row.row-2, "Eating Habits"]
    appetite = df.at[specie_cell_row.row-2, "Appetite"]
    image_url = df.at[specie_cell_row.row-2, "Image URL"]
    video_url = df.at[specie_cell_row.row-2, "Video URL"]
    audio_url = df.at[specie_cell_row.row-2, "Audio URL"]
    """

    HTML = (
        "<html>"
        "<head>"
        "<meta charset=\"utf-8\">"
        "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">"
        "<link rel=\"icon\" type=\"image/x-icon\" href=\"https://living-taxonomy-media.s3.jp-tok.cloud-object-storage.appdomain.cloud/Logo.png\" >"
        "<title>" + common_name + " | Living Taxonomy" + "</title>"
        "</head>"
        
        "<h1><u>" + common_name + "</u></h1>"

        "<img src=\"" + image_url + "\"alt=\"" + common_name + "\"width=\"320\"\"height=\"240\"><br>"

        "<br>"
        "<br>"
        
        "<iframe src=\"" + video_url + "\" width=\"320\" height=\"240\" allow=\"autoplay\"></iframe>"
        
        "<br>"
        "<br>"

        "<audio controls> <source src=\"" + audio_url + "\"> </audio>"

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

    return HTML
