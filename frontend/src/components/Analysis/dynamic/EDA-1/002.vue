<template>
   <card class="pt-4">
        <div class="typography-line">
        <p>아래의 코드들은 개인적으로 사용하기 위해 만들어둔 함수들이다. 어떤 함수가 어떤 목적으로 작성되었는지는 전혀 몰라도 상관이 없다. 
        우리가 관심있는 것은 그저 어떤 분석을 했느냐에 다름아니니 말이다. 따라서 전혀보지 않아도 좋다.
        </p>
        </div>
        <div class="typography-line">
        <p>plotly 모듈을 이용하여 그래프를 그리기 위해 작성한 함수들이다. 그러나 축의 제목, 범위, 겹쳐그리기 등 커스터마이징 해야하는 부분이
            너무 많아 나중에는 잘 사용하지 않았다.
        </p>
        </div>
        <send-code number="3">
def seriesPlot(series, title=None, order=None, orderArray=None,color=False, colorScale = None, marker_color=False):<br>
&nbsp; &nbsp; if isinstance(orderArray, list):<br>
&nbsp; &nbsp; &nbsp; &nbsp; order = 'array'<br>
&nbsp; &nbsp; layoutVal ={'categoryorder':order, 'categoryarray' : orderArray}<br>
&nbsp; &nbsp; if color:<br>
&nbsp; &nbsp; &nbsp; &nbsp; colorVal = series.name<br>
&nbsp; &nbsp; else:<br>
&nbsp; &nbsp; &nbsp; &nbsp; colorVal = None<br>
&nbsp; &nbsp; fig = px.bar(series, y=series.name, x=series.index, color=colorVal, title=title, color_continuous_scale=colorScale)<br>
&nbsp; &nbsp; fig.update_layout(title_x=0.5, xaxis=layoutVal)<br>
&nbsp; &nbsp; fig['layout']['title']['font'] = dict(size=26)<br>
&nbsp; &nbsp; if marker_color:<br>
&nbsp; &nbsp; &nbsp; &nbsp; fig.update_traces(marker_color=['hsl('+str(h)+',50%'+',50%)' for h in np.linspace(0, 360, series.size)])<br>
&nbsp; &nbsp; return fig<br>
<br>
def dfPlot(df,x, y, title=None, order=None, orderArray=None ,color=False, colorScale = None, autoText = False):<br>
&nbsp; &nbsp; if isinstance(orderArray, list):<br>
&nbsp; &nbsp; &nbsp; &nbsp; order = 'array'<br>
&nbsp; &nbsp; layoutVal ={'categoryorder':order, 'categoryarray' : orderArray}<br>
&nbsp; &nbsp; colorVal = None<br>
&nbsp; &nbsp; if isinstance(y, list) and len(y)&gt;1:<br>
&nbsp; &nbsp; &nbsp; &nbsp; if color:<br>
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; colorVal = df.y<br>
&nbsp; &nbsp; &nbsp; &nbsp; fig = go.Figure(data=[<br>
&nbsp; &nbsp; &nbsp; &nbsp; go.Bar(name=y[i], x=x, y=df[y[i]], marker_color = colorScale[i] if colorScale else None) for i in range(len(y))<br>
&nbsp; &nbsp; &nbsp; &nbsp; ])<br>
&nbsp; &nbsp; &nbsp; &nbsp; fig.update_layout(barmode='group')<br>
&nbsp; &nbsp; else:<br>
&nbsp; &nbsp; &nbsp; &nbsp; if color:<br>
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; colorVal = y<br>
&nbsp; &nbsp; &nbsp; &nbsp; fig = px.bar(df,x=x, y=y, color=colorVal, color_continuous_scale=colorScale, text_auto=autoText)<br>
&nbsp; &nbsp; fig.update_layout(title_x=0.5, title=title, xaxis=layoutVal)<br>
&nbsp; &nbsp; fig['layout']['title']['font'] = dict(size=26)<br>
&nbsp; &nbsp; return fig<br>
<br>
def heatMapMap(x, y):<br>
&nbsp; &nbsp; m = folium.Map(location=(37.5776087830657, 126.976896737645), zoom_start=11)<br>
&nbsp; &nbsp;<br>
&nbsp; &nbsp; heatMap = HeatMap(zip(x, y),<br>
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;min_opacity=0.1,<br>
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;max_val=5,<br>
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;radius=10, blur=10,<br>
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;max_zoom=5,color='red')<br>
<br>
&nbsp; &nbsp; m.add_child(heatMap)<br>
&nbsp; &nbsp; return m<br>
<br>
def TimeSeriesPlot(df, freq, period, y, title=None, palette=True):<br>
&nbsp; &nbsp; fig = go.Figure()<br>
&nbsp; &nbsp; if palette:<br>
&nbsp; &nbsp; &nbsp; &nbsp; palette = px.colors.sequential.Sunsetdark<br>
&nbsp; &nbsp; else:<br>
&nbsp; &nbsp; &nbsp; &nbsp; palette = px.colors.sequential.Aggrnyl + px.colors.sequential.Agsunset + px.colors.sequential.algae + px.colors.sequential.amp + px.colors.sequential.Blackbody + px.colors.sequential.Bluered + px.colors.sequential.Blugrn + px.colors.sequential.Bluyl<br>
&nbsp; &nbsp; index = 0<br>
&nbsp; &nbsp; for window in plotdf[freq].unique():<br>
&nbsp; &nbsp; &nbsp; &nbsp; table= df.groupby(freq).get_group(window)<br>
&nbsp; &nbsp; &nbsp; &nbsp; fig.add_trace(go.Scatter(x=table[period], y=table[y], name=window, line=dict(color=palette[index], width=4)))<br>
&nbsp; &nbsp; &nbsp; &nbsp; index +=1<br>
<br>
&nbsp; &nbsp; fig.update_layout(title=title,<br>
&nbsp; &nbsp; xaxis_title=period,<br>
&nbsp; &nbsp; yaxis_title=y)<br>
&nbsp; &nbsp; return fig<br>
<br>
def HorizontalPortionBar(top_labels,x_data, y_data, colors=None, title=None):<br>
&nbsp; &nbsp; if not isinstance(colors, list):<br>
&nbsp; &nbsp; &nbsp; &nbsp; colors = px.colors.sequential.Sunsetdark<br>
&nbsp; &nbsp; x_data = [i/i.sum()*100 for i in x_data]<br>
&nbsp; &nbsp; x_data = [i.round(decimals=2) for i in x_data]<br>
&nbsp; &nbsp; fig = go.Figure()<br>
<br>
&nbsp; &nbsp; for i in range(0, len(x_data[0])):<br>
&nbsp; &nbsp; &nbsp; &nbsp; for xd, yd in zip(x_data, y_data):<br>
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; fig.add_trace(go.Bar(<br>
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; x=[xd[i]], y=[yd],<br>
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; orientation='h',<br>
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; marker=dict(<br>
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; color=colors[i],<br>
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; line=dict(color='rgb(248, 248, 249)', width=1)<br>
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; )<br>
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; ))<br>
<br>
&nbsp; &nbsp; fig.update_layout(<br>
&nbsp; &nbsp; &nbsp; &nbsp; title=title,<br>
&nbsp; &nbsp; &nbsp; &nbsp; xaxis=dict(<br>
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; showgrid=False,<br>
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; showline=False,<br>
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; showticklabels=False,<br>
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; zeroline=False,<br>
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; domain=[0.15, 1]<br>
&nbsp; &nbsp; &nbsp; &nbsp; ),<br>
&nbsp; &nbsp; &nbsp; &nbsp; yaxis=dict(<br>
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; showgrid=False,<br>
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; showline=False,<br>
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; showticklabels=False,<br>
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; zeroline=False,<br>
&nbsp; &nbsp; &nbsp; &nbsp; ),<br>
&nbsp; &nbsp; &nbsp; &nbsp; barmode='stack',<br>
&nbsp; &nbsp; &nbsp; &nbsp; paper_bgcolor='rgb(248, 248, 255)',<br>
&nbsp; &nbsp; &nbsp; &nbsp; plot_bgcolor='rgb(248, 248, 255)',<br>
&nbsp; &nbsp; &nbsp; &nbsp; margin=dict(l=120, r=10, t=140, b=80),<br>
&nbsp; &nbsp; &nbsp; &nbsp; showlegend=False,<br>
&nbsp; &nbsp; )<br>
<br>
&nbsp; &nbsp; annotations = []<br>
<br>
&nbsp; &nbsp; for yd, xd in zip(y_data, x_data):<br>
&nbsp; &nbsp; &nbsp; &nbsp; # labeling the y-axis<br>
&nbsp; &nbsp; &nbsp; &nbsp; annotations.append(dict(xref='paper', yref='y',<br>
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; x=0.14, y=yd,<br>
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; xanchor='right',<br>
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; text=str(yd),<br>
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; font=dict(family='Arial', size=14,<br>
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; color='rgb(67, 67, 67)'),<br>
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; showarrow=False, align='right'))<br>
&nbsp; &nbsp; &nbsp; &nbsp; # labeling the first percentage of each bar (x_axis)<br>
&nbsp; &nbsp; &nbsp; &nbsp; annotations.append(dict(xref='x', yref='y',<br>
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; x=xd[0] / 2, y=yd,<br>
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; text=str(xd[0]) + '%',<br>
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; font=dict(family='Arial', size=14,<br>
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; color='rgb(248, 248, 255)'),<br>
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; showarrow=False))<br>
&nbsp; &nbsp; &nbsp; &nbsp; # labeling the first Likert scale (on the top)<br>
&nbsp; &nbsp; &nbsp; &nbsp; if yd == y_data[-1]:<br>
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; annotations.append(dict(xref='x', yref='paper',<br>
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; x=xd[0] / 2, y=1.1,<br>
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; text=top_labels[0],<br>
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; font=dict(family='Arial', size=14,<br>
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; color='rgb(67, 67, 67)'),<br>
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; showarrow=False))<br>
&nbsp; &nbsp; &nbsp; &nbsp; space = xd[0]<br>
&nbsp; &nbsp; &nbsp; &nbsp; for i in range(1, len(xd)):<br>
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; # labeling the rest of percentages for each bar (x_axis)<br>
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; annotations.append(dict(xref='x', yref='y',<br>
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; x=space + (xd[i]/2), y=yd,<br>
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; text=str(xd[i]) + '%',<br>
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; font=dict(family='Arial', size=14,<br>
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; color='rgb(248, 248, 255)'),<br>
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; showarrow=False))<br>
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; # labeling the Likert scale<br>
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; if yd == y_data[-1]:<br>
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; annotations.append(dict(xref='x', yref='paper',<br>
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; x=space + (xd[i]/2), y=1.1,<br>
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; text=top_labels[i],<br>
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; font=dict(family='Arial', size=14,<br>
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; color='rgb(67, 67, 67)'),<br>
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; showarrow=False))<br>
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; space += xd[i]<br>
<br>
&nbsp; &nbsp; fig.update_layout(annotations=annotations)<br>
&nbsp; &nbsp; return fig<br>
<br>
def pivotToTimeplot(timeplotdf, title=None, yaxis = None, yRange=None, order = False, duration=500):<br>
&nbsp; &nbsp; variables = timeplotdf.index<br>
&nbsp; &nbsp; N=len(timeplotdf.columns)<br>
&nbsp; &nbsp; colorPalette = pd.Series(['hsl('+str(h)+',50%'+',50%)' for h in np.linspace(0, 360, N)], index=timeplotdf.iloc[-1].sort_values(ascending = False).index)<br>
&nbsp; &nbsp; if order:<br>
&nbsp; &nbsp; &nbsp; &nbsp;colorPalette = colorPalette.loc[timplotdf.columns]<br>
&nbsp; &nbsp; timeplotdf.iloc[-1].sort_values(ascending = False)<br>
<br>
&nbsp; &nbsp; columnOrder = timeplotdf.iloc[-1].sort_values(ascending = False).index if order else None;<br>
<br>
&nbsp; &nbsp; fig_dict = {<br>
&nbsp; &nbsp; &nbsp; &nbsp; "data": [],<br>
&nbsp; &nbsp; &nbsp; &nbsp; "layout": {},<br>
&nbsp; &nbsp; &nbsp; &nbsp; "frames": []<br>
&nbsp; &nbsp; }<br>
&nbsp; &nbsp; fig_dict["layout"]["xaxis"] = {"title": timeplotdf.columns.name}<br>
&nbsp; &nbsp; fig_dict["layout"]["yaxis"] = {"title": yaxis, "range": yRange}<br>
&nbsp; &nbsp; fig_dict["layout"]["hovermode"] = "closest"<br>
&nbsp; &nbsp; fig_dict["layout"]["updatemenus"] = [<br>
&nbsp; &nbsp; &nbsp; &nbsp; {<br>
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; "buttons": [<br>
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; {<br>
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; "args": [None, {"frame": {"duration": duration, "redraw": False},<br>
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; "fromcurrent": True, "transition": {"duration": duration,<br>
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; "easing": "quadratic-in-out"}}],<br>
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; "label": "Play",<br>
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; "method": "animate"<br>
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; },<br>
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; {<br>
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; "args": [[None], {"frame": {"duration": 0, "redraw": False},<br>
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; "mode": "immediate",<br>
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; "transition": {"duration": 0}}],<br>
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; "label": "Pause",<br>
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; "method": "animate"<br>
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; }<br>
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; ],<br>
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; "direction": "left",<br>
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; "pad": {"r": 10, "t": 87},<br>
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; "showactive": False,<br>
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; "type": "buttons",<br>
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; "x": 0.1,<br>
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; "xanchor": "right",<br>
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; "y": 0,<br>
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; "yanchor": "top"<br>
&nbsp; &nbsp; &nbsp; &nbsp; }<br>
&nbsp; &nbsp; ]<br>
&nbsp; &nbsp; sliders_dict = {<br>
&nbsp; &nbsp; &nbsp; &nbsp; "active": 0,<br>
&nbsp; &nbsp; &nbsp; &nbsp; "yanchor": "top",<br>
&nbsp; &nbsp; &nbsp; &nbsp; "xanchor": "left",<br>
&nbsp; &nbsp; &nbsp; &nbsp; "currentvalue": {<br>
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; "font": {"size": 20},<br>
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; "prefix": timeplotdf.index.name+":",<br>
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; "visible": True,<br>
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; "xanchor": "right"<br>
&nbsp; &nbsp; &nbsp; &nbsp; },<br>
&nbsp; &nbsp; &nbsp; &nbsp; "transition": {"duration": duration, "easing": "cubic-in-out"},<br>
&nbsp; &nbsp; &nbsp; &nbsp; "pad": {"b": 10, "t": 50},<br>
&nbsp; &nbsp; &nbsp; &nbsp; "len": 0.9,<br>
&nbsp; &nbsp; &nbsp; &nbsp; "x": 0.1,<br>
&nbsp; &nbsp; &nbsp; &nbsp; "y": 0,<br>
&nbsp; &nbsp; &nbsp; &nbsp; "steps": []<br>
&nbsp; &nbsp; }<br>
<br>
&nbsp; &nbsp; variable = variables[0]<br>
&nbsp; &nbsp; data = go.Bar(x=timeplotdf.columns, y=timeplotdf.loc[variable], marker_color=colorPalette)<br>
&nbsp; &nbsp; data_dict = {<br>
&nbsp; &nbsp; &nbsp; &nbsp; "x": timeplotdf.columns,<br>
&nbsp; &nbsp; &nbsp; &nbsp; "y": timeplotdf.loc[variable]<br>
&nbsp; &nbsp; }<br>
&nbsp; &nbsp; fig_dict["data"].append(data)<br>
<br>
<br>
&nbsp; &nbsp; for variable in variables:<br>
&nbsp; &nbsp; &nbsp; &nbsp; frame = {"data": [], "name": str(variable)}<br>
&nbsp; &nbsp; &nbsp; &nbsp; data = go.Bar(x=timeplotdf.columns, y=timeplotdf.loc[variable])<br>
&nbsp; &nbsp; &nbsp; &nbsp; data_dict = {<br>
&nbsp; &nbsp; &nbsp; &nbsp; "x": timeplotdf.columns,<br>
&nbsp; &nbsp; &nbsp; &nbsp; "y": timeplotdf.loc[variable],<br>
&nbsp; &nbsp; &nbsp; &nbsp; }<br>
&nbsp; &nbsp; &nbsp; &nbsp; frame["data"].append(data)<br>
<br>
&nbsp; &nbsp; &nbsp; &nbsp; fig_dict["frames"].append(frame)<br>
&nbsp; &nbsp; &nbsp; &nbsp; slider_step = {"args": [<br>
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; [variable],<br>
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; {"frame": {"duration": duration, "redraw": False},<br>
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;"mode": "immediate",<br>
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;"transition": {"duration": duration}}<br>
&nbsp; &nbsp; &nbsp; &nbsp; ],<br>
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; "label": variable,<br>
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; "method": "animate"}<br>
&nbsp; &nbsp; &nbsp; &nbsp; sliders_dict["steps"].append(slider_step)<br>
<br>
&nbsp; &nbsp; fig_dict["layout"]["sliders"] = [sliders_dict]<br>
&nbsp; &nbsp; fig_dict['layout']['title'] = title<br>
&nbsp; &nbsp; fig_dict['layout']['xaxis']['categoryorder'] = 'array'<br>
&nbsp; &nbsp; fig_dict['layout']['xaxis']['categoryarray'] = columnOrder<br>
<br>
&nbsp; &nbsp; fig = go.Figure(fig_dict)<br>
&nbsp; &nbsp; return fig<br>
<br>
<br>
def pxMerger(figs, rows, cols):<br>
&nbsp; &nbsp; fig = make_subplots(rows=rows, cols=cols, shared_xaxes=False)<br>
&nbsp; &nbsp; N = rows*cols<br>
&nbsp; &nbsp; for i in range(min(N, len(figs))):<br>
&nbsp; &nbsp; &nbsp; &nbsp; fig.add_trace(figs[i]['data'][0], row=i//cols+1, col=i%cols+1)<br>
&nbsp; &nbsp; fig.update_layout( &nbsp; <br>
&nbsp; &nbsp; width=400*cols+500,<br>
&nbsp; &nbsp; height = 300*rows+300)<br>
&nbsp; &nbsp; return fig<br>
<br>
def errorIntepreter(errors, models, trialset, draw='RMSLE', log=False, parameter='alpha', title=None, compare=None):<br>
&nbsp; &nbsp; figs = []<br>
&nbsp; &nbsp; for i in range(len(models)):<br>
&nbsp; &nbsp; &nbsp; &nbsp; model_error = pd.DataFrame(errors[models[i]], columns=['RMSLE', 'RMSE', 'MAE'], index=trialset)<br>
&nbsp; &nbsp; &nbsp; &nbsp; figs.append(px.line(model_error, x=model_error.index, y=draw, log_x=log))<br>
&nbsp; &nbsp; fig = pxMerger(figs, len(models), 1)<br>
&nbsp; &nbsp; for i in range(len(models)):<br>
&nbsp; &nbsp; &nbsp; &nbsp; fig.update_yaxes(title_text=models[i]().__class__.__name__, row=i+1, col=1)<br>
&nbsp; &nbsp; &nbsp; &nbsp; if log:<br>
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; fig.update_xaxes(type="log", row=1+i, col=1)<br>
&nbsp; &nbsp; if log:<br>
&nbsp; &nbsp; &nbsp; &nbsp; fig.update_xaxes(title_text=parameter, type="log", row=len(models), col=1)<br>
&nbsp; &nbsp; else:<br>
&nbsp; &nbsp; &nbsp; &nbsp; fig.update_xaxes(title_text=parameter, row=len(models), col=1)<br>
&nbsp; &nbsp; fig.update_layout(title_text=title)<br>
&nbsp; &nbsp; if isinstance(compare, float) or isinstance(compare, int):<br>
&nbsp; &nbsp; &nbsp; &nbsp; shapes = [{'type' : "line",'x0' : min(trialset), 'y0' : compare, 'x1' : max(trialset), 'y1': compare,'line' : {'color' : "Red","width":2, "dash":"dashdot"}, 'xref': 'x1', 'yref': 'y'+str(i+1)} for i in range(len(models)) ]<br>
&nbsp; &nbsp; &nbsp; &nbsp; fig['layout'].update(shapes=shapes)<br>
&nbsp; &nbsp; return fig<br>
        </send-code>
        <div class="typography-line">
        <p>이 함수들은 모델에 대한 평가를 자동화하기 위해 만든 함수들이다. 그러나 이것들도 나중에는 잘 쓰지 않았다.</p>
        </div>
        <send-code number="4">
            def minMaxScale(df):<br>
&nbsp; &nbsp; min_max_scaler = MinMaxScaler()<br>
&nbsp; &nbsp; min_max_scaler.fit(df)<br>
&nbsp; &nbsp; scaled_df = min_max_scaler.transform(df)<br>
&nbsp; &nbsp; scaled_df = pd.DataFrame(scaled_df, columns=df.columns, index=df.index)<br>
&nbsp; &nbsp; return scaled_df<br>
<br>
def evaluation(y,pred):<br>
&nbsp; &nbsp; rmsle_val = np.sqrt(np.mean((np.log1p(y) - np.log1p(pred)) ** 2))<br>
&nbsp; &nbsp; rmse_val = np.sqrt(mean_squared_error(y,pred))<br>
&nbsp; &nbsp; mae_val = mean_absolute_error(y,pred)<br>
&nbsp; &nbsp; print('RMSLE: {0:.3f}, RMSE: {1:.3F}, MAE: {2:.3F}'.format(rmsle_val, rmse_val, mae_val))<br>
&nbsp; &nbsp; return rmsle_val, rmse_val, mae_val<br>
&nbsp; &nbsp;<br>
def get_top_error(y_test, pred, n_tops = 5):<br>
&nbsp; &nbsp; result_df = pd.DataFrame(y_test.values, columns=['real_count'])<br>
&nbsp; &nbsp; result_df['predicted_count']= np.round(pred)<br>
&nbsp; &nbsp; result_df['diff'] = np.abs(result_df['real_count'] - result_df['predicted_count'])<br>
&nbsp; &nbsp; print(result_df.sort_values('diff', ascending=False)[:n_tops])<br>
&nbsp; &nbsp;<br>
def model_evaluation(model, X, y, translation='', test_times=3, test_size=24*30*6, watch=False, output = 'error'):<br>
&nbsp; &nbsp; if translation=='log1p' :<br>
&nbsp; &nbsp; &nbsp; &nbsp; y = np.log1p(y)<br>
&nbsp; &nbsp; if translation=='sqrt' :<br>
&nbsp; &nbsp; &nbsp; &nbsp; y = np.sqrt(y)<br>
&nbsp; &nbsp; if translation=='cbrt' :<br>
&nbsp; &nbsp; &nbsp; &nbsp; y = np.cbrt(y)<br>
&nbsp; &nbsp; if translation=='qqrt' :<br>
&nbsp; &nbsp; &nbsp; &nbsp; y = np.sqrt(np.sqrt(y))<br>
&nbsp; &nbsp; tscv = TimeSeriesSplit(n_splits=test_times , test_size=test_size)<br>
&nbsp; &nbsp; for train_index, test_index in tscv.split(X):<br>
&nbsp; &nbsp; &nbsp; &nbsp; X_train, X_test = X.iloc[train_index], X.iloc[test_index]<br>
&nbsp; &nbsp; &nbsp; &nbsp; y_train, y_test = y.iloc[train_index], y.iloc[test_index]<br>
&nbsp; &nbsp; model.fit(X_train, y_train)<br>
&nbsp; &nbsp; pred = model.predict(X_test)<br>
&nbsp; &nbsp; if translation=='log1p' :<br>
&nbsp; &nbsp; &nbsp; &nbsp; y_test = np.expm1(y_test)<br>
&nbsp; &nbsp; &nbsp; &nbsp; pred = np.expm1(pred)<br>
&nbsp; &nbsp; if translation=='sqrt' :<br>
&nbsp; &nbsp; &nbsp; &nbsp; y_test = y_test**2<br>
&nbsp; &nbsp; &nbsp; &nbsp; pred = pred**2<br>
&nbsp; &nbsp; if translation=='cbrt' :<br>
&nbsp; &nbsp; &nbsp; &nbsp; y_test = y_test**3<br>
&nbsp; &nbsp; &nbsp; &nbsp; pred = pred**3<br>
&nbsp; &nbsp; if translation=='qqrt' :<br>
&nbsp; &nbsp; &nbsp; &nbsp; y_test = y_test**4<br>
&nbsp; &nbsp; &nbsp; &nbsp; pred = pred**4<br>
&nbsp; &nbsp; if watch:<br>
&nbsp; &nbsp; &nbsp; &nbsp; get_top_error(y_test, pred, n_tops = 5)<br>
&nbsp; &nbsp; print('###',model.__class__.__name__,'###')<br>
&nbsp; &nbsp; if output =='model':<br>
&nbsp; &nbsp; &nbsp; &nbsp; return model<br>
&nbsp; &nbsp; return evaluation(y_test, pred)<br>
<br>
def rmsle(y, pred):<br>
&nbsp; &nbsp; return np.sqrt(np.mean((np.log1p(y) - np.log1p(pred)) ** 2))<br>
<br>
def rmse(y,pred):<br>
&nbsp; &nbsp; return np.sqrt(mean_squared_error(y,pred))<br>
<br>
def mae(y,pred):<br>
&nbsp; &nbsp; return mean_absolute_error(y,pred)<br>
<br>
        </send-code>
        <div class="typography-line">
        <p>csv파일을 읽어들이기 위해 만든 함수이다. 이 함수들은 한 번 작성된 후, 변경하지 않고 끝까지 잘 사용했다.</p>
        </div>
        <send-code number="5">
def getAllCsv(subDir, data_dir=data_dir):<br>
&nbsp; &nbsp; if(subDir[-1]!='/'):<br>
&nbsp; &nbsp; &nbsp; &nbsp; subDir += '/'<br>
&nbsp; &nbsp; if(subDir[0]=='/'):<br>
&nbsp; &nbsp; &nbsp; &nbsp; subDir = subDir[1:]<br>
&nbsp; &nbsp; A = []<br>
&nbsp; &nbsp; for fileName in os.listdir(data_dir+subDir):<br>
&nbsp; &nbsp; &nbsp; &nbsp; try:<br>
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; print(fileName)<br>
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; a =pd.read_csv(data_dir+subDir+fileName, encoding='cp949', index_col=0)<br>
&nbsp; &nbsp; &nbsp; &nbsp; except:<br>
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; print(fileName)<br>
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; a =pd.read_csv(data_dir+subDir+fileName, encoding='utf-8', index_col=0)<br>
&nbsp; &nbsp; &nbsp; &nbsp; A.append(a)<br>
&nbsp; &nbsp; return A<br>
<br>
def getAllCsvDask(subDir, data_dir=data_dir, dtype=None):<br>
&nbsp; &nbsp; if(subDir[-1]!='/'):<br>
&nbsp; &nbsp; &nbsp; &nbsp; subDir += '/'<br>
&nbsp; &nbsp; if(subDir[0]=='/'):<br>
&nbsp; &nbsp; &nbsp; &nbsp; subDir = subDir[1:]<br>
&nbsp; &nbsp; A = []<br>
&nbsp; &nbsp; for fileName in os.listdir(data_dir+subDir):<br>
&nbsp; &nbsp; &nbsp; &nbsp; print(fileName)<br>
&nbsp; &nbsp; &nbsp; &nbsp; try:<br>
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; dask_df = dd.read_csv(data_dir+subDir+fileName, encoding='cp949', dtype=dtype)<br>
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; pandas_df = dask_df.compute()<br>
&nbsp; &nbsp; &nbsp; &nbsp; except:<br>
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; print(fileName)<br>
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; dask_df = dd.read_csv(data_dir+subDir+fileName, encoding='UTF-8', dtype=dtype)<br>
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; pandas_df = dask_df.compute()<br>
&nbsp; &nbsp; &nbsp; &nbsp; A.append(pandas_df)<br>
&nbsp; &nbsp; return A<br>
        </send-code>
        <div class="typography-line">
        <p>머신러닝시에 데이터셋을 빌드하고 GridSearchCV를 수행할 때, 교차검증하기에는 적은 수의 데이터만을 가지고 있는
            대여소들의 경우를 상정하고 만든 함수이다.
        </p>
        </div>
        <send-code number="6">
def getSpotData(number): &nbsp;#데이터 전처리과정 포함<br>
&nbsp; &nbsp; data = pd.concat([대여반납_2019[대여반납_2019['대여소']==number], 대여반납_2020[대여반납_2020['대여소']==number],<br>
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;대여반납_2021[대여반납_2021['대여소']==number], 대여반납_2022[대여반납_2022['대여소']==number]], ignore_index=True, axis=0)<br>
&nbsp; &nbsp; open_day = pd.to_datetime(share_spot.loc[share_spot['대여소번호']==number, '대여소신설일']).iloc[0]<br>
&nbsp; &nbsp; since_day = (pd.to_datetime(weather['일시'])-open_day).dt.days<br>
&nbsp; &nbsp; since_day.name = '경과일'<br>
&nbsp; &nbsp; weather_since = pd.concat([weather ,since_day], axis=1)<br>
&nbsp; &nbsp; data = pd.merge(left=data, right=weather_since.loc[weather_since['경과일']&gt;=0], how='right', left_on = ['년','월','일','시'], right_on=['년','월','일','시']).drop(['일','년','월','휴일_x','시'], axis=1)<br>
&nbsp; &nbsp; data['대여횟수'] = data['대여횟수'].fillna(0)<br>
&nbsp; &nbsp; data['반납횟수'] = data['반납횟수'].fillna(0)<br>
&nbsp; &nbsp; data['대여소'] = data['대여소'].fillna(number)<br>
&nbsp; &nbsp; mms = MinMaxScaler()<br>
&nbsp; &nbsp; scaled_rows = pd.DataFrame(mms.fit_transform(data.loc[:,['기온', '풍속(m/s)','전운량(10분위)', '습도(%)', '경과일']]))<br>
&nbsp; &nbsp; data['기온'] = scaled_rows[0]<br>
&nbsp; &nbsp; data['풍속'] = scaled_rows[1]<br>
&nbsp; &nbsp; data['전운량'] = scaled_rows[2]<br>
&nbsp; &nbsp; data['습도'] = scaled_rows[3]<br>
&nbsp; &nbsp; data['경과일'] = scaled_rows[4]<br>
&nbsp; &nbsp; data['강수량'] = np.log1p(data.loc[:,['강수량(mm)']])<br>
&nbsp; &nbsp; data.drop(['풍속(m/s)','전운량(10분위)', '습도(%)', '강수량(mm)'], axis=1, inplace=True)<br>
&nbsp; &nbsp; data.columns = ['대여소','대여횟수', '반납횟수', '일시', '기온', '안개', '비 또는 눈', '연무', '휴일', '경과일', '풍속', '전운량', '습도', '강수량']<br>
&nbsp; &nbsp; data.index = pd.to_datetime(data['일시'])<br>
&nbsp; &nbsp; data['일시'] = pd.to_datetime(data['일시'])<br>
&nbsp; &nbsp; return data<br>
<br>
class GridSearchWithoutCV:<br>
&nbsp; &nbsp; def __init__(self, estimator, param_grid , scoring):<br>
&nbsp; &nbsp; &nbsp; &nbsp; self.best_score = float('inf')<br>
&nbsp; &nbsp; &nbsp; &nbsp; self.estimator = estimator<br>
&nbsp; &nbsp; &nbsp; &nbsp; self.parameters = ParameterGrid(param_grid)<br>
&nbsp; &nbsp; &nbsp; &nbsp; sefl.scoring = scoring<br>
&nbsp; &nbsp; &nbsp; &nbsp; self.best_estimator = None<br>
&nbsp; &nbsp;<br>
&nbsp; &nbsp; def bestFit(self, x, y, test_x, test_y):<br>
&nbsp; &nbsp; &nbsp; &nbsp; for g in self.parameters:<br>
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; self.estimator.set_params(**g)<br>
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; self.estimator.fit(x, y)<br>
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; pred = estimator.predict(test_x) &nbsp; &nbsp; &nbsp; <br>
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; error_val = self.scoring(test_y,pred)<br>
&nbsp; &nbsp; &nbsp; &nbsp; if error_val &lt; best_score:<br>
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; best_score = error_val<br>
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; best_grid = g<br>
&nbsp; &nbsp; &nbsp; &nbsp; self.best_estimator = estimator.set_params(**best_grid)<br>
&nbsp; &nbsp; def best_estimator_(self):<br>
&nbsp; &nbsp; &nbsp; &nbsp; return self.best_estimator<br>
&nbsp; &nbsp;<br>
def MachineLearn(X,y, models, model_names, params, ohe=True, analysis='유출량', method=''):<br>
&nbsp; &nbsp; len_in_year = len(X)/24/365<br>
&nbsp; &nbsp; if len_in_year &gt; 3.49:<br>
&nbsp; &nbsp; &nbsp; &nbsp; test_len = 24*6*30<br>
&nbsp; &nbsp; &nbsp; &nbsp; cross_validation_N = 4<br>
&nbsp; &nbsp; elif len_in_year &gt; 2.99:<br>
&nbsp; &nbsp; &nbsp; &nbsp; test_len = 24*6*30<br>
&nbsp; &nbsp; &nbsp; &nbsp; cross_validation_N = 3<br>
&nbsp; &nbsp; elif len_in_year &gt; 2.49:<br>
&nbsp; &nbsp; &nbsp; &nbsp; test_len = 24*6*30<br>
&nbsp; &nbsp; &nbsp; &nbsp; cross_validation_N = 2 &nbsp;<br>
&nbsp; &nbsp; elif len_in_year &gt; 1.95:<br>
&nbsp; &nbsp; &nbsp; &nbsp; test_len = 24*4*30<br>
&nbsp; &nbsp; &nbsp; &nbsp; cross_validation_N = 3<br>
&nbsp; &nbsp; elif len_in_year &gt; 1.6:<br>
&nbsp; &nbsp; &nbsp; &nbsp; test_len = 24*4*30<br>
&nbsp; &nbsp; &nbsp; &nbsp; cross_validation_N = 2 <br>
&nbsp; &nbsp; elif len_in_year &gt; 1.3:<br>
&nbsp; &nbsp; &nbsp; &nbsp; test_len = int(len(X_ohe)*0.2)<br>
&nbsp; &nbsp; &nbsp; &nbsp; cross_validation_N = 1<br>
&nbsp; &nbsp; train_len = len(X)-test_len<br>
&nbsp; &nbsp; if ohe:<br>
&nbsp; &nbsp; &nbsp; &nbsp; ohe_cal = []<br>
&nbsp; &nbsp; &nbsp; &nbsp; for cal in ['년', '월','시','요일']:<br>
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; if cal in X.columns:<br>
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; ohe_cal.append(cal)<br>
&nbsp; &nbsp; &nbsp; &nbsp; X_ohe = pd.get_dummies(X, columns=ohe_cal)<br>
&nbsp; &nbsp; &nbsp; &nbsp; X_train = X_ohe[:train_len]<br>
&nbsp; &nbsp; &nbsp; &nbsp; X_test = X_ohe[train_len:]<br>
&nbsp; &nbsp; else:<br>
&nbsp; &nbsp; &nbsp; &nbsp; X_train = X[:train_len]<br>
&nbsp; &nbsp; &nbsp; &nbsp; X_test = X[train_len:]<br>
&nbsp; &nbsp; y['유출량'] = y['대여횟수']-y['반납횟수']<br>
&nbsp; &nbsp; y_train = y[:train_len]<br>
&nbsp; &nbsp; y_test = y[train_len:]<br>
&nbsp; &nbsp; y_train_유출량 = y_train[analysis]<br>
&nbsp; &nbsp; y_test_유출량 = y_test[analysis]<br>
&nbsp; &nbsp; if method == 'cbrt':<br>
&nbsp; &nbsp; &nbsp; &nbsp; y_train_유출량 = np.cbrt(y_train_유출량)<br>
&nbsp; &nbsp; &nbsp; &nbsp; y_test_유출량 = np.cbrt(y_test_유출량)<br>
&nbsp; &nbsp; if cross_validation_N &gt; 1:<br>
&nbsp; &nbsp; &nbsp; &nbsp; tscv = TimeSeriesSplit(n_splits=cross_validation_N, test_size=test_len)<br>
&nbsp; &nbsp;<br>
&nbsp; &nbsp; error_names = ['RMSE', 'MAE']<br>
&nbsp; &nbsp; fit_models = {}<br>
&nbsp; &nbsp; models_point = np.empty(shape=[0])<br>
&nbsp; &nbsp; best_mae = float('inf')<br>
&nbsp; &nbsp; for model_name, model in models:<br>
&nbsp; &nbsp; &nbsp; &nbsp; param_grid = params[model_name]<br>
&nbsp; &nbsp; &nbsp; &nbsp; if cross_validation_N &gt; 1:<br>
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; grid = GridSearchCV(estimator=model, cv=tscv, param_grid=param_grid, scoring="neg_mean_absolute_error", verbose=10) <br>
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; grid = grid.fit(X_train, y_train_유출량)<br>
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; model = grid.best_estimator_<br>
&nbsp; &nbsp; &nbsp; &nbsp; else:<br>
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; grid = GridSearchWithoutCV(estimator=model, param_grid=param_grid, scoring = mae)<br>
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; grid = grid.fit(X_train, y_train_대여, X_test, y_test_대여)<br>
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; model = grid.best_estimator_<br>
&nbsp; &nbsp; &nbsp; &nbsp; pred = model.predict(X_test)<br>
&nbsp; &nbsp; &nbsp; &nbsp;<br>
&nbsp; &nbsp; &nbsp; &nbsp; if method=='cbrt':<br>
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; rmse_val = rmse(y_test_유출량**3,pred**3)<br>
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; mae_val = mean_absolute_error(y_test_유출량**3, pred**3) &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; <br>
&nbsp; &nbsp; &nbsp; &nbsp; else:<br>
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; rmse_val = rmse(y_test_유출량,pred)<br>
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; mae_val = mean_absolute_error(y_test_유출량, pred)<br>
&nbsp; &nbsp; &nbsp; &nbsp; if best_mae &gt; mae_val:<br>
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; best_model = model<br>
&nbsp; &nbsp; &nbsp; &nbsp; fit_models[model_name] = model<br>
&nbsp; &nbsp; &nbsp; &nbsp; print(model_name)<br>
&nbsp; &nbsp; &nbsp; &nbsp; print('RMSE: {0:.3F}, MAE: {1:.3F}'.format(rmse_val, mae_val))<br>
&nbsp; &nbsp; &nbsp; &nbsp; models_point = np.concatenate((models_point, rmse_val, mae_val), axis = None)<br>
&nbsp; &nbsp; models_error = pd.DataFrame(models_point.reshape(-1,2),columns=error_names, index = model_names)<br>
&nbsp; &nbsp; best_models = fit_models<br>
&nbsp; &nbsp;<br>
&nbsp; &nbsp;<br>
&nbsp; &nbsp; best_pred = best_model.predict(X_test)<br>
&nbsp; &nbsp; if method=='cbrt':<br>
&nbsp; &nbsp; &nbsp; &nbsp; y_test_유출량 = (y_test_유출량)**3<br>
&nbsp; &nbsp; &nbsp; &nbsp; best_pred = best_pred**3<br>
&nbsp; &nbsp; pred_comparison = pd.concat([y_test_유출량.reset_index(drop=True), pd.Series(best_pred)], axis=1)<br>
&nbsp; &nbsp; pred_comparison.columns = [analysis, '예측']<br>
&nbsp; &nbsp; pred_comparison[1:40] &nbsp; <br>
&nbsp; &nbsp; fig = go.Figure()<br>
&nbsp; &nbsp; fig.add_trace(go.Scatter(y=pred_comparison[1:40][analysis],<br>
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; mode='lines+markers',<br>
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; name=analysis))<br>
&nbsp; &nbsp; fig.add_trace(go.Scatter(y=pred_comparison[1:40]['예측'],<br>
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; mode='lines',<br>
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; name='예측'))<br>
&nbsp; &nbsp; fig.update_layout(<br>
&nbsp; &nbsp; &nbsp; &nbsp; title_text="BEST 예측과 실제 "+analysis +' '+ method,<br>
&nbsp; &nbsp; &nbsp; &nbsp; )<br>
<br>
&nbsp; &nbsp; fig.show()<br>
&nbsp; &nbsp; return best_models, models_error, pred_comparison<br>
<br>
def errorplot(errors, upper, lower, title, error='MAE'):<br>
&nbsp; &nbsp; fig = px.line(errors[error] , markers=True)<br>
&nbsp; &nbsp; fig.update_layout(<br>
&nbsp; &nbsp; &nbsp; &nbsp; title_text=title,<br>
&nbsp; &nbsp; &nbsp; &nbsp; )<br>
&nbsp; &nbsp; fig.add_trace(go.Scatter(<br>
&nbsp; &nbsp; &nbsp; &nbsp; x=errors['MAE'].index,<br>
&nbsp; &nbsp; &nbsp; &nbsp; y=[upper]*len(errors),<br>
&nbsp; &nbsp; &nbsp; &nbsp; name="'---' model"<br>
&nbsp; &nbsp; ))<br>
&nbsp; &nbsp; fig.add_trace(go.Scatter(<br>
&nbsp; &nbsp; &nbsp; &nbsp; x=errors['MAE'].index,<br>
&nbsp; &nbsp; &nbsp; &nbsp; y=[lower]*len(errors),<br>
&nbsp; &nbsp; &nbsp; &nbsp; name="all time best"<br>
&nbsp; &nbsp; ))<br>
&nbsp; &nbsp; return fig <br>
<br>
def getSpotData(number):<br>
&nbsp; &nbsp; data = pd.concat([대여반납_2019[대여반납_2019['대여소']==number], 대여반납_2020[대여반납_2020['대여소']==number],<br>
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;대여반납_2021[대여반납_2021['대여소']==number], 대여반납_2022[대여반납_2022['대여소']==number]], ignore_index=True, axis=0)<br>
&nbsp; &nbsp; open_day = pd.to_datetime(share_spot.loc[share_spot['대여소번호']==number, '대여소신설일']).iloc[0]<br>
&nbsp; &nbsp; weather['일시'] = pd.to_datetime(weather['일시'])<br>
&nbsp; &nbsp; since_day = (weather['일시']-open_day).dt.days<br>
&nbsp; &nbsp; since_day.name = '경과일'<br>
&nbsp; &nbsp; weather_since = pd.concat([weather ,since_day], axis=1)<br>
&nbsp; &nbsp; data = pd.merge(left=data, right=weather_since.loc[weather_since['경과일']&gt;=0], how='right', left_on = ['년','월','일','시'], right_on=['년','월','일','시']).drop(['일시','대여소','일','휴일_x'], axis=1)<br>
&nbsp; &nbsp; data['대여횟수'] = data['대여횟수'].fillna(0)<br>
&nbsp; &nbsp; data['반납횟수'] = data['반납횟수'].fillna(0)<br>
&nbsp; &nbsp; data.columns = ['시', '대여횟수', '반납횟수', '년', '월', '기온', '강수량(mm)', '풍속(m/s)',<br>
&nbsp; &nbsp; &nbsp; &nbsp;'습도(%)', '전운량(10분위)', '안개', '비 또는 눈', '연무', '휴일', '경과일']<br>
<br>
&nbsp; &nbsp; return data<br>
        </send-code>


   </card>
    
</template>
<script>
import sendCode from 'src/components/Analysis/sendCode.vue';
import receiveCode from 'src/components/Analysis/recieveCode.vue'

export default {
   name : 'dynamic-002',
  components: {
    sendCode,
    receiveCode
  },
  data() {
    return {

    };
  }
};
</script>