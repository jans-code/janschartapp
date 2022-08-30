import streamlit as st
import datetime
import time
import util
import json

st.set_page_config(page_title='Jans Chart App', page_icon='🎧', layout='wide', initial_sidebar_state='collapsed')

st.markdown(
     f"""
     <style>
     .stApp {{
         background-image: url("https://www.janarman.de/chartapp/chart_background.jpg");
         background-attachment: fixed;
         background-size: cover
     }}
     #MainMenu {{visibility: hidden;}}
     footer {{visibility: hidden;}}
     </style>
     """,
     unsafe_allow_html=True
    )

if "startup_message" not in st.session_state:
    st.session_state["startup_message"] = True

st.sidebar.title('')

todays_date = datetime.date(datetime.date.today().year,datetime.date.today().month,datetime.date.today().day)

historic = st.sidebar.date_input('Datum wählen', min_value=datetime.date(1977,1,3), 
            max_value=todays_date)

if historic != todays_date:
    st.session_state["startup_message"] = False

st.sidebar.markdown("![JAP Design](https://www.janarman.de/chartapp/chart_japfiaed.png)")

st.sidebar.caption("Alle Daten werden von www.offiziellecharts.de bereitgestellt. " \
                    "Neue Charts erscheinen Freitags um 16 Uhr, allerdings werden bis Mittwoch nicht alle Plätze angezeigt. ")

user_time = str(round(time.mktime(historic.timetuple())*1000))

left_space, content, right_space = st.columns([0.125, 0.75, 0.125])

content.markdown("![Jans Chart App](https://www.janarman.de/chartapp/chart_header.gif)")

single_tab, album_tab, compilation_tab, hiphop_tab, dance_tab = content.tabs(['Single','Album', 'Compilation',
                                                                           'Hiphop', 'Dance'])
single_charts = util.get_the_charts('single',100,user_time)
table = util.build_table(single_charts, True, True)
if st.session_state["startup_message"]:
    single_tab.warning('📆 Um frühere Charts anzuzeigen wähle ein Datum in der Sidebar (oben links auf > klicken)')
single_tab.header('Deutsche Single Charts')
chart_date = 'Charts vom '+str(single_charts[-1]['updated'])
single_tab.caption(chart_date)
single_tab.markdown(table)
single_json = util.create_export_json(single_charts, 'Deutsche Single Charts')
single_tab.write('')
single_tab.download_button('Download JSON',json.dumps(single_json,indent=4), file_name=f"single_{str(single_charts[-1]['updated'])}_export.json")

album_charts = util.get_the_charts('album',100,user_time)
table = util.build_table(album_charts, True, False)
album_tab.header('Deutsche Album Charts')
chart_date = 'Charts vom '+str(album_charts[-1]['updated'])
album_tab.caption(chart_date)
album_tab.markdown(table)
album_json = util.create_export_json(album_charts, 'Deutsche Album Charts')
album_tab.write('')
album_tab.download_button('Download JSON',json.dumps(album_json,indent=4), file_name=f"album_{str(album_charts[-1]['updated'])}_export.json")

compilation_charts = util.get_the_charts('compilation',30, user_time)
table = util.build_table(compilation_charts, False, False)
compilation_tab.header('Deutsche Compilation Charts')
chart_date = 'Charts vom '+str(compilation_charts[-1]['updated'])
compilation_tab.caption(chart_date)
compilation_tab.markdown(table)
compilation_json = util.create_export_json(compilation_charts, 'Deutsche Compilation Charts')
compilation_tab.write('')
compilation_tab.download_button('Download JSON',json.dumps(compilation_json,indent=4), file_name=f"compilation_{str(compilation_charts[-1]['updated'])}_export.json")

hiphop_charts = util.get_the_charts('hiphop',20, user_time)
table = util.build_table(hiphop_charts, True, False)
hiphop_tab.header('Deutsche Hiphop Charts')
chart_date = 'Charts vom '+str(hiphop_charts[-1]['updated'])
hiphop_tab.caption(chart_date)
hiphop_tab.markdown(table)
hiphop_json = util.create_export_json(hiphop_charts, 'Deutsche Hiphop Charts')
hiphop_tab.write('')
hiphop_tab.download_button('Download JSON',json.dumps(hiphop_json,indent=4), file_name=f"hiphop_{str(hiphop_charts[-1]['updated'])}_export.json")

dance_charts = util.get_the_charts('dance',20, user_time)
table = util.build_table(dance_charts, True, False)
dance_tab.header('Deutsche Dance Charts')
chart_date = 'Charts vom '+str(dance_charts[-1]['updated'])
dance_tab.caption(chart_date)
dance_tab.markdown(table)
dance_json = util.create_export_json(dance_charts, 'Deutsche Dance Charts')
dance_tab.write('')
dance_tab.download_button('Download JSON',json.dumps(dance_json,indent=4), file_name=f"dance_{str(dance_charts[-1]['updated'])}_export.json")
