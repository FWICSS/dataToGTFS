import streamlit as st
import pandas as pd

# Liste des colonnes GTFS stops
list_columns_gtfs_stops = [
    'stop_id', 'stop_code', 'stop_name', 'stop_desc', 'stop_lat',
    'stop_lon', 'zone_id', 'stop_url', 'location_type',
    'parent_station', 'stop_timezone', 'wheelchair_boarding'
]
list_columns_gtfs_stops_description = ['Code de l\'ârret', 'Nom de l\'arrêt', 'Description de l\'arrêt',
                                       'Latitude de l\'arrêt', 'Longitude de l\'arrêt', 'Ville de l\'arrêt',
                                       'URL de l\'arrêt', 'Type de localisation', 'Station parente',
                                       'Fuseau horaire de l\'arrêt', 'Accès en fauteuil roulant']


def load_file(uploaded_file):
    if uploaded_file.name.endswith('.csv'):
        df = pd.read_csv(uploaded_file)
    elif uploaded_file.name.endswith('.txt'):
        df = pd.read_csv(uploaded_file, delimiter='\t')
    elif uploaded_file.name.endswith('.xls') or uploaded_file.name.endswith('.xlsx'):
        df = pd.read_excel(uploaded_file)
    else:
        st.error("Unsupported file format")
        return None
    return df


def main():
    st.title("Visionneuse de colonnes de fichiers")
    st.write("Téléchargez un fichier TXT, CSV ou XLS/XLSX pour voir les colonnes.")

    uploaded_file = st.file_uploader("Choisissez un fichier", type=['txt', 'csv', 'xls', 'xlsx'])

    if uploaded_file is not None:
        df = load_file(uploaded_file)
        if df is not None:
            st.write("Colonnes du fichier:")
            st.write(df.columns.tolist())

            st.write("Faites correspondre les colonnes de votre fichier aux colonnes d'arrêts GTFS.")

            column_mapping = {}
            selected_columns = set()

            for index, col in enumerate(list_columns_gtfs_stops[1:]):
                available_options = [None] + [column for column in df.columns if column not in selected_columns]
                selected_column = st.selectbox(
                    f"Sélectionnez la colonne pour {list_columns_gtfs_stops_description[index]}", available_options,
                    key=col)
                column_mapping[col] = selected_column
                if selected_column:
                    selected_columns.add(selected_column)

            st.write("Correspondance des colonnes:")
            st.write(column_mapping)

            if st.button("Générer le fichier XLSX"):
                output_df = pd.DataFrame(columns=list_columns_gtfs_stops)

                for gtfs_col, file_col in column_mapping.items():
                    if file_col:
                        output_df[gtfs_col] = df[file_col]
                    else:
                        output_df[gtfs_col] = pd.NA

                output_file = "output_gtfs_stops.xlsx"
                output_df.to_excel(output_file, index=False)
                st.success(f"Le fichier {output_file} a été généré avec succès.")
                with open(output_file, "rb") as f:
                    st.download_button("Télécharger le fichier XLSX", f, file_name=output_file)


if __name__ == "__main__":
    main()
