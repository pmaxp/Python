#import library 
import pandas as pd
import plotly.graph_objects as go

def funnel_through(df, u_id, event_name, date_time, list_events, list_events_text, title, through=False, img=False):
    
    #создаем сводную таблицу
    step_data_pivot = df.pivot_table(index=u_id, #user_id, devaice_id ... _id
                                   columns=event_name, #event_name
                                   values=date_time, #event_date
                                   aggfunc='min')
    
    counts_step = len(list_events)#определяем кол-во шагов
    steps = {}#создаем словарь шагов
    steps[0] = ~step_data_pivot[list_events[0]].isna()#первый шаг воронки проверка на не пустое значение
    if through:
        for i in range(0,len(list_events)-1):#остальные шаги
            steps[i+1] = steps[0] & (~step_data_pivot[list_events[i+1]].isna())
        #проверяем True предыдущего шага и что есть два следущих события True и они идут друг за другом
    else:
        for i in range(0,len(list_events)-1):#остальные шаги
            steps[i+1] = steps[i] & (step_data_pivot[list_events[i+1]] > step_data_pivot[list_events[i]])
        #проверяем True предыдущего шага и что есть два следущих события True и они идут друг за другом
    steps_sum = [sum(steps[x]) for x in steps.keys()]#считаем сумму
    
    df_steps = pd.DataFrame(steps_sum, index=list_events_text, columns=['quantity']) #собираем в таблицу
    df_steps['ratio 100%'] = round(df_steps['quantity']/df_steps['quantity'][0] * 100) #добавляем % от первого события
    df_steps['ratio %'] = (round(df_steps['quantity'].pct_change(),2) + 1) * 100 #добавляем % от предыдущего шага
    display(df_steps) #выводим таблицу можно сделать return если не нужна визуализация
    
    if img:
        #делаем график воронки
        fig = go.Figure(go.Funnel(
        y = df_steps.index,
        x = df_steps['quantity']
        ))
        fig.update_layout(title=title)
        fig.show()
