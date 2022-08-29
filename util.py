import datetime
import time
import urllib3

def remove_endspan(work_data):
    return work_data.split('</span>')[0]

def get_the_charts(url_part, chart_length, user_time):   
    http = urllib3.PoolManager()
    url = 'https://www.offiziellecharts.de/charts/'+url_part+'/for-date-'+user_time
    r = http.request('get', url)
    chart_data = r.data.decode('utf-8')
    chart_data = chart_data.split('Zeitraum:')[1]
    chart_date = chart_data.split('<strong>')[1][:10]
    d_chart = ''
    for i in range(0,3,1):
        d_chart += chart_date.split('.')[i]+'.'
    d_chart = d_chart[:-1]
    d_chart_string = str(d_chart)        
    chart_list = []
    for i in range(1,chart_length+1):
        try:
            buffer = chart_data.split('<span class="this-week">')
            thisweek_position = remove_endspan(buffer[i])
            thisweek_position = thisweek_position.replace(' ', '')
            buffer = chart_data.split('<span class="last-week">')
            lastweek_position = remove_endspan(buffer[i])
            lastweek_position = lastweek_position[2:]
            lastweek_position = lastweek_position.replace(' ', '')
            if lastweek_position == '':
                lastweek_position = '-'
                position = "**" + thisweek_position + "** ![new](https://www.janarman.de/chartapp/chart_new.png)" + " " + lastweek_position
            elif lastweek_position == thisweek_position:
                position = "**" + thisweek_position + "** ![equal](https://www.janarman.de/chartapp/chart_equal.png)" + " *" + lastweek_position + "*"
            elif int(lastweek_position) > int(thisweek_position):
                position = "**" + thisweek_position + "** ![up](https://www.janarman.de/chartapp/chart_up.png)" + " ~~" + lastweek_position + "~~"
            elif int(lastweek_position) < int(thisweek_position):
                position = "**" + thisweek_position + "** ![down](https://www.janarman.de/chartapp/chart_down.png)" + " ~~" + lastweek_position + "~~"
            buffer = chart_data.split(' <span class="info-artist">')
            artist_name = remove_endspan(buffer[i])
            buffer = chart_data.split(' <span class="info-title">')
            title_name = remove_endspan(buffer[i])
            title_name = title_name.replace('\\','')
            search_string = f'{artist_name}+{title_name}'
            for elem in [(',',' '),('\t', ''), ('/', ''), (' & ', '+'), ('  ', '+'), (' ', '+'), ('&', '')]:
                search_string = search_string.replace(elem[0],elem[1])
            if search_string[-1] == ' ':
                search_string = search_string[:-1]
            search_string2 = search_string.replace('+','%20')
            chart_list.append({'artist_name': artist_name,
                'title_name': title_name,
                'position': position,
                'search_string': search_string,
                'search_string2': search_string2,
                'thisweek_position': thisweek_position,
                'lastweek_position': lastweek_position})
        except:
            break
    chart_list.append({'updated' : d_chart_string})
            
    return chart_list

def build_table(chart_list, include_title, include_youtube):
    table = '|Platz|'
    if include_title:
        table += '*Titel* / Interpret|'
    else:
        table += 'Titel|'
    table += 'Suche|\n|-----|-----|'
    table += '-----|\n'
    for i in range(len(chart_list)-1):
        table += f"{chart_list[i]['position']}|"
        if include_title:
            if chart_list[i]['title_name'][-1] == ' ':
                chart_list[i]['title_name'] += chart_list[i]['title_name'][:-1]
            table += f"*{chart_list[i]['title_name']}* / "
        table += f"{chart_list[i]['artist_name']}|"
        if include_youtube:
            table += f"[![YT Link](https://www.janarman.de/chartapp/chart_yt.png)]"
            table += f"(https://www.youtube.com/results?search_query={chart_list[i]['search_string']}) "
        else:
            table += f"[![AMZN Link](https://www.janarman.de/chartapp/chart_amzn.png)]"
            table += f"(https://www.amazon.de/s?k={chart_list[i]['search_string']}) "
        search_elements = [f"[![SPTFY Link](https://www.janarman.de/chartapp/chart_spotify.png)]",
                            f"(https://open.spotify.com/search/{chart_list[i]['search_string2']}) ",
                            f"[![APPLM Link](https://www.janarman.de/chartapp/chart_applm.png)]",
                            f"(https://music.apple.com/de/search?term={chart_list[i]['search_string']}) ",
                            f"[![AMZNM Link](https://www.janarman.de/chartapp/chart_amznmsc.png)]",
                            f"(https://music.amazon.de/search/{chart_list[i]['search_string']})"
                        ]
        for elem in search_elements:
            table += elem
        table += "|\n"
    return table

def create_export_json(chart_list, chart_name):
    export = {'name': chart_name, 
            'date': chart_list[-1]['updated'],
             'charts': [{'thisweek_position':chart_list[i]['thisweek_position'],
                        'lastweek_position':chart_list[i]['lastweek_position'],
                        'title_name':chart_list[i]['title_name'],
                        'artist_name':chart_list[i]['artist_name'],
                        } for i in range(len(chart_list)-1)]
            }
    return export