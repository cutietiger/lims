from Products.Five.browser import BrowserView
from plone import api
from datetime import datetime
import json

def date2json(obj):
    if isinstance(obj,datetime):
        epoch = datetime.utcfromtimestamp(0)
        return int((obj - epoch).total_seconds()) * 1000
    raise TypeError('%r is not JSON serializable' % obj) 

class DashboardView(BrowserView):
    """ A list of talks
    """

    def bar(self, title):
        options = {
            'chart': {
                'type': 'bar'
            },
            'title': {
                'text': title
            },
            'xAxis': {
                'categories': ['Apples', 'Bananas', 'Oranges']
            },
            'yAxis': {
                'title': {
                    'text': 'Fruit eaten'
                }
            },
            'series': [{
                'name': 'Grace',
                'data': [1, 0, 4]
            }, {
                'name': 'Robert',
                'data': [5, 7, 3]
            }]
        }
        return json.dumps(options)

    def spline(self, title):
        options = {
            'chart': {
                'type': 'spline'
            },
            'title': {
                'text': title
            },
            'xAxis': {
                'type': 'datetime',
                'title': {
                    'text': 'Date'
                }
            },
            'yAxis': {
                'title': {
                    'text': 'Result'
                },
                'min': 0
             },
             'tooltip': {
                 'crosshairs': True,
                 'shared': True
             },
             'plotOptions': {
                 'spline': {
                     'marker': {
                         'enabled': True
                     }
                 }
             },
             'series': [{
                 'name': 'Total 25-OHD',
                 'data': [[datetime(1970,9,3), 55.0], [datetime(1970,9,28), 20.0], 
                          [datetime(1970,10,18),0.0], 
                          [datetime(1970,11,11),2.0], [datetime(1970,12,2),33.0]]
                 }, {
                 'name': 'Vit D3',
                 'data': [[datetime(1970,9,3), 55.0], [datetime(1970,10,18),30.0], 
                         [datetime(1970,11,11),2.0], [datetime(1970,12,2),30.0]]
                 }, {
                 'name': 'Vit D2',
                 'data': [[datetime(1970,9,3), 55.0], [datetime(1970,10,18),5.0], 
                         [datetime(1970,11,11),2.0], [datetime(1970,12,2),3.0]]
                 }]
        }
        return json.dumps(options,default=date2json)

