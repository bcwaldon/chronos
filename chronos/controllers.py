
import httplib2
import pyramid.view
import pyramid.response

from chronos import models




class Controller(object):

    @pyramid.view.view_config(route_name='index', renderer='index.mako')
    def index(self, request):
        return {}

    @pyramid.view.view_config(route_name='graph')
    def graph(self, request):
        window = int(request.GET.get('window', 3600))
        results = models.ResultCollection(db=request.db, window=window)
        x_values = [str(m.begin_timestamp) for m in results]
        y_values = [str(m.duration) for m in results]
        x_value_str = ','.join(x_values)
        y_value_str = ','.join(y_values)
        x_value_min = min(x_values)
        x_value_max = max(x_values)
        y_value_min = min(y_values)
        y_value_max = max(y_values)

        url = 'http://chart.apis.google.com/chart?cht=lxy&chs=700x300&chd=t:%(x_value_str)s|%(y_value_str)s&chxr=0,%(x_value_min)s,%(x_value_max)s|1,%(y_value_min)s,%(y_value_max)s&chxt=x,y&chds=%(x_value_min)s,%(x_value_max)s,%(y_value_min)s,%(y_value_max)s'
        http = httplib2.Http()
        resp, content = http.request(url % locals())

        return pyramid.response.Response(body=content, content_type='image/jpeg')

