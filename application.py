from __future__ import print_function
from flask import Flask, render_template, request
# import boto3
import time
import os
import pandas as pd

from matplotlib.figure import Figure

from sklearn.cluster import KMeans

from bokeh.embed import components
from bokeh.plotting import figure
from bokeh.resources import INLINE
from bokeh.util.string import encode_utf8

application = Flask(__name__)
application.config.from_object('config')

# S3 instance
# s3_client = boto3.client('s3',
#                          aws_access_key_id=application.config['AWS_ACCESS_KEY_ID'],
#                          aws_secret_access_key=application.config['AWS_SECRET_ACCESS_KEY'])
#
# s3_resource = boto3.resource('s3',
#                          aws_access_key_id=application.config['AWS_ACCESS_KEY_ID'],
#                          aws_secret_access_key=application.config['AWS_SECRET_ACCESS_KEY'])


# get data
def getData():
    file_path = os.path.join(application.root_path, 'static', 'data2.csv')
    data = pd.read_csv(file_path, header=0)
    return data

def k_meansclustering(columns, num_clusters=5):
    data = get_data()
    X = data[list(columns)]
    X = X.as_matrix()
    start = time.time()
    km = KMeans(n_clusters=num_clusters, init="k-means++", max_iter=300, random_state=0)
    y_km = km.fit_predict(X)
    end = time.time()
    total_time = (end - start) * 1000
    centroids = km.cluster_centers_
    num_points_cluster = []
    for i in range(num_clusters):
        num_points_cluster.append(len(X[y_km == i, 0]))
    len_num_points_cluster = len(num_points_cluster)

    return (centroids.tolist(), num_points_cluster, len_num_points_cluster, total_time)


@application.route('/', methods=['GET','POST'])
def init_method():
    if request.method == 'GET':
        return render_template('first_page.html')
    elif request.method == 'POST':
        data1 = getData()
        numofent = data1.shape[0] # num of rows
        return render_template('first_page.html', numOfEnt=numofent)

        # return render_template('first_page.html', query=result, numOfEnt=res[0][0])

@application.route('/kmeans', methods=['GET','POST'])
def k_means_cluster():
    if request.method == 'GET':
        return render_template("k_means_cluster.html")
    elif request.method == 'POST':
        col1_name = 'House'
        col2_name = 'District'

        k_value = 6

        # getting data

        data = getData()

        X = data[[col1_name,col2_name]]
        X = X.as_matrix()

        time_before = time.time()
        #kmeans part
        km = KMeans(n_clusters=k_value, init='k-means++', n_init=10, max_iter=300, random_state=0)
        y_km = km.fit_predict(X)

        time_after = time.time()

        cur_time = (time_after - time_before) * 1000

        centroids = list(km.cluster_centers_)
        cluster_points_first = []
        cluster_points_second = []

        for i in range(k_value):
            cluster_points_first.append(len(X[y_km == i, 0]))
            cluster_points_second.append(len(X[y_km==i, 1]))
        len_num_points_cluster = len(cluster_points_first)

        return render_template('k_means_cluster.html',datainfo=centroids, ttr=cur_time, clusterpointsOne=cluster_points_first, clusterpointsTwo=cluster_points_second, lenofcluster=len_num_points_cluster)

@application.route('/kmeansinput', methods=['GET','POST'])
def k_means_input():
    if (request.method == 'GET'):
        return render_template("kmeans_input.html")
    else:
        col1_name = request.form['col1'] # User Input Column one
        col2_name = request.form['col2'] # User Input Column Two

        k_value = int(request.form['kvalue']) # User input K_Value

        # getting data

        data = getData()

        X = data[[col1_name, col2_name]]
        X = X.as_matrix()

        time_before = time.time()
        # kmeans part
        km = KMeans(n_clusters=k_value, init='k-means++', n_init=10, max_iter=300, random_state=0)
        y_km = km.fit_predict(X)

        time_after = time.time()

        cur_time = (time_after - time_before) * 1000

        centroids = list(km.cluster_centers_)
        cluster_points_first = []
        cluster_points_second = []

        for i in range(k_value):
            cluster_points_first.append(len(X[y_km == i, 0]))
            cluster_points_second.append(len(X[y_km == i, 1]))
        len_num_points_cluster = len(cluster_points_first)

        return render_template('kmeans_input.html', datainfo=centroids, ttr=cur_time, clusterpointsOne=cluster_points_first, clusterpointsTwo=cluster_points_second,
                               lenofcluster=len_num_points_cluster)

@application.route('/kmeansgraph', methods=['GET','POST'])
def k_means_graph():
    if (request.method == 'GET'):
        return render_template("kmeans_graph.html")
    elif (request.method == 'POST'):
        col1_name = request.form['col1']  # User Input Column one
        col2_name = request.form['col2']  # User Input Column Two

        k_value = int(request.form['kvalue'])  # User input K_Value

        # getting data

        data = getData()

        X = data[[col1_name, col2_name]]
        X = X.as_matrix()

        #time_before = time.time()
        # kmeans part
        km = KMeans(n_clusters=k_value, init='k-means++', n_init=10, max_iter=300, random_state=0)
        y_km = km.fit_predict(X)

        #time_after = time.time()

        #cur_time = (time_after - time_before) * 1000

        centroids = list(km.cluster_centers_)
        cluster_points_first = []
        cluster_points_second = []

        for i in range(k_value):
            cluster_points_first.append(len(X[y_km == i, 0]))
            cluster_points_second.append(len(X[y_km == i, 1]))
        #len_num_points_cluster = len(cluster_points_first)

        fig = figure(title="Scatter Plot")
        for i in range(k_value):
            for j in range(1):
                fig.scatter(centroids[i][j], centroids[i][j + 1], fill_color="red")
        js_files = INLINE.render_js()
        css_files = INLINE.render_css()
        script, div = components(fig)
        render_html = render_template('kmeans_graph.html', plot_script=script, plot_div=div, js_files=js_files,
                               css_files=css_files)
        return encode_utf8(render_html)

@application.route('/kmeanschart', methods=['GET','POST'])
def k_means_graph():
    if (request.method == 'GET'):
        return render_template("kmean_chart.html")
    elif (request.method == 'POST'):
        col1_name = request.form['col1']  # User Input Column one
        col2_name = request.form['col2']  # User Input Column Two

        k_value = int(request.form['kvalue'])  # User input K_Value

        # getting data

        data = getData()

        X = data[[col1_name, col2_name]]
        X = X.as_matrix()

        #time_before = time.time()
        # kmeans part
        km = KMeans(n_clusters=k_value, init='k-means++', n_init=10, max_iter=300, random_state=0)
        y_km = km.fit_predict(X)

        #time_after = time.time()

        #cur_time = (time_after - time_before) * 1000

        centroids = list(km.cluster_centers_)
        cluster_points_first = []
        cluster_points_second = []

        for i in range(k_value):
            cluster_points_first.append(len(X[y_km == i, 0]))
            cluster_points_second.append(len(X[y_km == i, 1]))
        #len_num_points_cluster = len(cluster_points_first)

        fig = figure(title="Scatter Plot")
        for i in range(k_value):
            for j in range(1):
                fig.scatter(centroids[i][j], centroids[i][j + 1], fill_color="red")
        js_files = INLINE.render_js()
        css_files = INLINE.render_css()
        script, div = components(fig)
        # define starts/ends for wedges from percentages of a circle
        percents = [0, 0.3, 0.4, 0.6, 0.9, 1]
        starts = [p * 2 * pi for p in percents[:-1]]
        ends = [p * 2 * pi for p in percents[1:]]

        # a color for each pie piece
        colors = ["red", "green", "blue", "orange", "yellow"]

        p = figure(x_range=(-1, 1), y_range=(-1, 1))

        p.wedge(x=0, y=0, radius=1, start_angle=starts, end_angle=ends, color=colors)

        # display/save everythin
        output_file("pie.html")
        show(p)
        render_html = render_template('kmeans_graph.html', plot_script=script, plot_div=div, js_files=js_files,
                               css_files=css_files)
        return encode_utf8(render_html)

if __name__ == '__main__':
    application.run(debug=True)
