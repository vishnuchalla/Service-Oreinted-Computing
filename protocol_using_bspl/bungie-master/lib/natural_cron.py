__all__ = ['natural_cron']

# Don't look below, you will not understand this Python code :) I don't.

from js2py.pyjs import *
# setting scope
var = Scope( JS_BUILTINS )
set_global_object(var)

# Code follows:
var.registers([])
@Js
def PyJs_anonymous_0_(this, arguments, var=var):
    var = Scope({'this':this, 'arguments':arguments}, var)
    var.registers([])
    def PyJs_LONG_42_(var=var):
        @Js
        def PyJs_anonymous_1_(this, arguments, var=var):
            var = Scope({'this':this, 'arguments':arguments}, var)
            var.registers([])
            pass
        PyJs_anonymous_1_._set_name('anonymous')
        @Js
        def PyJs_anonymous_2_(j, k, this, arguments, var=var):
            var = Scope({'j':j, 'k':k, 'this':this, 'arguments':arguments}, var)
            var.registers(['m', 'H', 'A', 'x', 'k', 'E', 'v', 'j', 'G', 'F', 'C', 'K', 'D', 'w', 'B', 'J', 'q', 's', 'I', 'y', 'z'])
            @Js
            def PyJsHoisted_m_(L, M, N, this, arguments, var=var):
                var = Scope({'L':L, 'M':M, 'N':N, 'this':this, 'arguments':arguments}, var)
                var.registers(['O', 'N', 'M', 'L'])
                var.put('O', var.get('q')(var.get('L')))
                while 1:
                    SWITCHED = False
                    CONDITION = (var.get('O'))
                    if SWITCHED or PyJsStrictEq(CONDITION, Js('frequencyWith')):
                        SWITCHED = True
                        return var.get('E')(var.get('L'), var.get('M'), var.get('N'))
                        break
                    if SWITCHED or PyJsStrictEq(CONDITION, Js('frequencyOnly')):
                        SWITCHED = True
                        return var.get('D')(var.get('L'), var.get('M'), var.get('N'))
                        break
                    if SWITCHED or PyJsStrictEq(CONDITION, Js('clockTime')):
                        SWITCHED = True
                        return var.get('B')(var.get('L'), var.get('M'), var.get('N'))
                        break
                    if SWITCHED or PyJsStrictEq(CONDITION, Js('day')):
                        SWITCHED = True
                        return var.get('C')(var.get('L'), var.get('M'), var.get('N'))
                        break
                    if SWITCHED or PyJsStrictEq(CONDITION, Js('minute')):
                        SWITCHED = True
                        return var.get('H')(var.get('L'), var.get('M'), var.get('N'))
                        break
                    if SWITCHED or PyJsStrictEq(CONDITION, Js('hour')):
                        SWITCHED = True
                        return var.get('F')(var.get('L'), var.get('M'), var.get('N'))
                        break
                    if SWITCHED or PyJsStrictEq(CONDITION, Js('month')):
                        SWITCHED = True
                        return var.get('G')(var.get('L'), var.get('M'), var.get('N'))
                        break
                    if SWITCHED or PyJsStrictEq(CONDITION, Js('year')):
                        SWITCHED = True
                        return var.get('K')(var.get('L'), var.get('M'), var.get('N'))
                        break
                    if SWITCHED or PyJsStrictEq(CONDITION, Js('rangeStart')):
                        SWITCHED = True
                        return var.get('I')(var.get('L'), var.get('M'), var.get('N'))
                        break
                    if SWITCHED or PyJsStrictEq(CONDITION, Js('rangeEnd')):
                        SWITCHED = True
                        return var.get('J')(var.get('L'), var.get('M'), var.get('N'))
                    SWITCHED = True
                    break
                return Js(0.0).neg()
            PyJsHoisted_m_.func_name = 'm'
            var.put('m', PyJsHoisted_m_)
            @Js
            def PyJsHoisted_q_(L, this, arguments, var=var):
                var = Scope({'L':L, 'this':this, 'arguments':arguments}, var)
                var.registers(['O', 'N', 'M', 'L'])
                var.put('M', Js('decideState'))
                for PyJsTemp in var.get('s'):
                    var.put('N', PyJsTemp)
                    var.put('O', var.get('RegExp').create(var.get('s').get(var.get('N')).get('regextest'), Js('ig')))
                    if var.get('O').callprop('test', var.get('L')):
                        var.put('M', var.get('N'))
                        break
                return var.get('M')
            PyJsHoisted_q_.func_name = 'q'
            var.put('q', PyJsHoisted_q_)
            Js('use strict')
            pass
            pass
            var.put('s', var.get('j')(Js('./maps')).get('regexString'))
            var.put('v', var.get('j')(Js('./maps')).get('defaultFlags'))
            var.put('w', var.get('j')(Js('./maps')).get('defaultResultCron'))
            var.put('x', var.get('j')(Js('./maps')).get('flags'))
            var.put('y', var.get('j')(Js('./maps')).get('resultCron'))
            var.put('z', var.get('j')(Js('readline')))
            var.put('A', var.get('j')(Js('./tokens')).get('tokenizeInput'))
            var.put('B', var.get('j')(Js('./states/clocktime')).get('getClockTime'))
            var.put('C', var.get('j')(Js('./states/day')).get('getDay'))
            var.put('D', var.get('j')(Js('./states/frequency')).get('getFrequencyOnly'))
            var.put('E', var.get('j')(Js('./states/frequency')).get('getFrequencyWith'))
            var.put('F', var.get('j')(Js('./states/hour')).get('getHour'))
            var.put('G', var.get('j')(Js('./states/month')).get('getMonth'))
            var.put('H', var.get('j')(Js('./states/minute')).get('getMinute'))
            var.put('I', var.get('j')(Js('./states/range')).get('rangeStartState'))
            var.put('J', var.get('j')(Js('./states/range')).get('rangeEndState'))
            var.put('K', var.get('j')(Js('./states/year')).get('getYear'))
            @Js
            def PyJs_anonymous_3_(M, N, this, arguments, var=var):
                var = Scope({'M':M, 'N':N, 'this':this, 'arguments':arguments}, var)
                var.registers(['S', 'O', 'M', 'P', 'Q', 'R', 'N'])
                def PyJs_LONG_4_(var=var):
                    return PyJsComma(PyJsComma(PyJsComma(PyJsComma(PyJsComma(PyJsComma(PyJsComma(PyJsComma(PyJsComma(PyJsComma(PyJsComma(var.put('N', (Js('MIN HOR DOM MON WEK YER') if (Js('undefined')==var.get('N',throw=False).typeof()) else var.get('N'))),var.get('x').put('isRangeForDay', var.get('v').get('isRangeForDay'))),var.get('x').put('isRangeForMonth', var.get('v').get('isRangeForMonth'))),var.get('x').put('isRangeForYear', var.get('v').get('isRangeForYear'))),var.get('x').put('isRangeForHour', var.get('v').get('isRangeForHour'))),var.get('x').put('isRangeForMin', var.get('v').get('isRangeForMin'))),var.get('y').put('min', var.get('w').get('min'))),var.get('y').put('hour', var.get('w').get('hour'))),var.get('y').put('day_of_month', var.get('w').get('day_of_month'))),var.get('y').put('month', var.get('w').get('month'))),var.get('y').put('day_of_week', var.get('w').get('day_of_week'))),var.get('y').put('year', var.get('w').get('year')))
                PyJs_LONG_4_()
                var.put('O', Js([]))
                var.put('P', Js(''))
                var.put('Q', var.get('A')(var.get('M')))
                ((var.get(u"null")==var.get('Q')) and var.put('P', Js('Please enter human readable rules !\n'), '+'))
                var.put('R', Js(0.0).neg())
                #for JS loop
                var.put('S', Js(0.0))
                while (var.get('R') and (var.get('S')<var.get('Q').get('length'))):
                    try:
                        var.put('R', var.get('m')(var.get('Q').get(var.get('S')), var.get('O'), var.get('P')))
                    finally:
                            (var.put('S',Js(var.get('S').to_number())+Js(1))-Js(1))
                def PyJs_LONG_6_(var=var):
                    def PyJs_LONG_5_(var=var):
                        return (((Js('ERROR:')+var.get('P'))+Js('\t\t'))+var.get('N').callprop('replace', Js('MIN'), var.get('y').get('min')).callprop('replace', Js('HOR'), var.get('y').get('hour')).callprop('replace', Js('DOM'), var.get('y').get('day_of_month')).callprop('replace', Js('MON'), var.get('y').get('month')).callprop('replace', Js('WEK'), var.get('y').get('day_of_week')).callprop('replace', Js('YER'), var.get('y').get('year')))
                    return (PyJs_LONG_5_() if (Js(1.0).neg()==var.get('R')) else var.get('N').callprop('replace', Js('MIN'), var.get('y').get('min')).callprop('replace', Js('HOR'), var.get('y').get('hour')).callprop('replace', Js('DOM'), var.get('y').get('day_of_month')).callprop('replace', Js('MON'), var.get('y').get('month')).callprop('replace', Js('WEK'), var.get('y').get('day_of_week')).callprop('replace', Js('YER'), var.get('y').get('year')))
                return PyJs_LONG_6_()
            PyJs_anonymous_3_._set_name('anonymous')
            var.get('k').put('exports', PyJs_anonymous_3_)
        PyJs_anonymous_2_._set_name('anonymous')
        @Js
        def PyJs_anonymous_7_(j, k, this, arguments, var=var):
            var = Scope({'j':j, 'k':k, 'this':this, 'arguments':arguments}, var)
            var.registers(['v', 'j', 'q', 'w', 's', 'k'])
            Js('use strict')
            var.put('q', Js({'isRangeForDay':Js(1.0).neg(),'isRangeForMonth':Js(1.0).neg(),'isRangeForYear':Js(1.0).neg(),'isRangeForHour':Js(1.0).neg(),'isRangeForMin':Js(1.0).neg()}))
            var.put('s', Js({'min':Js('*'),'hour':Js('*'),'day_of_month':Js('*'),'month':Js('*'),'day_of_week':Js('?'),'year':Js('*')}))
            var.put('v', Js({'isRangeForDay':var.get('q').get('isRangeForDay'),'isRangeForMonth':var.get('q').get('isRangeForMonth'),'isRangeForYear':var.get('q').get('isRangeForYear'),'isRangeForHour':var.get('q').get('isRangeForHour'),'isRangeForMin':var.get('q').get('isRangeForMin')}))
            var.put('w', Js({'min':var.get('s').get('min'),'hour':var.get('s').get('hour'),'day_of_month':var.get('s').get('day_of_month'),'month':var.get('s').get('month'),'day_of_week':var.get('s').get('day_of_week'),'year':var.get('s').get('year')}))
            def PyJs_LONG_8_(var=var):
                return var.get('k').put('exports', Js({'regexString':Js({'every':Js({'regextest':Js('^(every|each|all|entire)$')}),'clockTime':Js({'regextest':Js('^([0-9]+:)?[0-9]+ *(AM|PM)$|^([0-9]+:[0-9]+)$|(noon|midnight)'),'regexexec':Js([Js('^[0-9]+'), Js(':[0-9]+'), Js('pm'), Js('am'), Js('(noon|midnight)')])}),'year':Js({'regextest':Js('((years|year)|([0-9]{4}[0-9]*(( ?and)?,? ?))+)'),'regexexec':Js([Js('^(years|year)$'), Js('[0-9]*'), Js('^[0-9]{4}$')])}),'frequencyWith':Js({'regextest':Js('^[0-9]+(th|nd|rd|st)$')}),'frequencyOnly':Js({'regextest':Js('^[0-9]+$'),'regexexec':Js('^[0-9]+')}),'minute':Js({'regextest':Js('(minutes|minute|mins|min)'),'regexexec':Js([Js('^(minutes|minute|mins|min)$')])}),'hour':Js({'regextest':Js('(hour|hrs|hours)'),'regexexec':Js([Js('^(hour|hrs|hours)$')])}),'day':Js({'regextest':Js('^((days|day)|(((monday|tuesday|wednesday|thursday|friday|saturday|sunday|WEEKEND|MON|TUE|WED|THU|FRI|SAT|SUN)( ?and)?,? ?)+))$'),'regexexec':Js([Js('^(day|days)$'), Js('(MON|TUE|WED|THU|FRI|SAT|SUN|WEEKEND)')])}),'month':Js({'regextest':Js('^((months|month)|(((january|february|march|april|may|june|july|august|september|october|november|december|JAN|FEB|MAR|APR|MAY|JUN|JUL|AUG|SEPT|OCT|NOV|DEC)( ?and)?,? ?)+))$'),'regexexec':Js([Js('^(month|months)$'), Js('(JAN|FEB|MAR|APR|MAY|JUN|JUL|AUG|SEPT|OCT|NOV|DEC)')])}),'rangeStart':Js({'regextest':Js('(between|starting|start)')}),'rangeEnd':Js({'regextest':Js('(to|through|ending|end|and)')}),'tokenising':Js({'regexexec':Js('(hour|hrs|hours)|(minutes|minute|mins|min)|((months|month)|(((january|february|march|april|may|june|july|august|september|october|november|december|JAN|FEB|MAR|APR|MAY|JUN|JUL|AUG|SEPT|OCT|NOV|DEC)( ?and)?,? ?)+))|[0-9]+(th|nd|rd|st)|(([0-9]+:)?[0-9]+( +)?(AM|PM))|([0-9]+:[0-9]+)|(noon|midnight)|((days|day)|(((monday|tuesday|wednesday|thursday|friday|saturday|sunday|WEEKEND|MON|TUE|WED|THU|FRI|SAT|SUN)( ?and)?,? ?)+))|(([0-9]{4}[0-9]*(( ?and)?,? ?))+)|([0-9]+)|(to|through|ending|end|and)|(between|starting|start)')})}),'defaultFlags':var.get('q'),'defaultResultCron':var.get('s'),'flags':var.get('v'),'resultCron':var.get('w')}))
            PyJs_LONG_8_()
        PyJs_anonymous_7_._set_name('anonymous')
        @Js
        def PyJs_anonymous_9_(j, k, this, arguments, var=var):
            var = Scope({'j':j, 'k':k, 'this':this, 'arguments':arguments}, var)
            var.registers(['v', 'j', 'q', 's', 'k'])
            Js('use strict')
            var.put('q', var.get('j')(Js('../maps')).get('regexString'))
            var.put('s', var.get('j')(Js('../maps')).get('flags'))
            var.put('v', var.get('j')(Js('../maps')).get('resultCron'))
            @Js
            def PyJs_anonymous_10_(w, x, y, this, arguments, var=var):
                var = Scope({'w':w, 'x':x, 'y':y, 'this':this, 'arguments':arguments}, var)
                var.registers(['D', 'G', 'F', 'C', 'w', 'x', 'B', 'A', 'y', 'z', 'E'])
                var.put('z', var.get('RegExp').create(var.get('q').get('clockTime').get('regexexec').get('0')))
                var.put('A', var.get('w').callprop('match', var.get('z')))
                def PyJs_LONG_11_(var=var):
                    return PyJsComma(PyJsComma(PyJsComma(var.put('B', (var.get('parseInt')(var.get('A').get('0')) if ((var.get(u"null")!=var.get('A')) and (Js(0.0)<var.get('A').get('length'))) else Js(0.0))),var.put('z', var.get('RegExp').create(var.get('q').get('clockTime').get('regexexec').get('1')))),var.put('A', var.get('z').callprop('exec', var.get('w')))),((var.get(u"null")!=var.get('A')) and (Js(0.0)<var.get('A').get('length'))).neg())
                if PyJs_LONG_11_():
                    var.put('C', Js(0.0))
                else:
                    if ((-Js(1.0))==var.get('A').get('0').callprop('indexOf', Js(':'))):
                        var.put('C', Js(0.0))
                    else:
                        if PyJsComma(var.put('C', var.get('parseInt')(var.get('A').get('0').callprop('slice', (var.get('A').get('0').callprop('indexOf', Js(':'))+Js(1.0))))),(Js(60.0)<=var.get('C'))):
                            return PyJsComma(var.put('y', Js(' please enter correct minutes !'), '+'),Js(1.0).neg())
                var.put('D', var.get('RegExp').create(var.get('q').get('clockTime').get('regexexec').get('2'), Js('ig')))
                var.put('E', var.get('RegExp').create(var.get('q').get('clockTime').get('regexexec').get('3'), Js('ig')))
                if var.get('D').callprop('test', var.get('w')):
                    if (Js(12.0)>var.get('B')):
                        var.put('B', Js(12.0), '+')
                    else:
                        if (Js(12.0)<var.get('B')):
                            return PyJsComma(var.put('y', Js(' please correct the time before PM !'), '+'),Js(1.0).neg())
                else:
                    if var.get('E').callprop('test', var.get('w')):
                        if (Js(12.0)==var.get('B')):
                            var.put('B', Js(0.0))
                        else:
                            if (Js(12.0)<var.get('B')):
                                return PyJsComma(var.put('y', Js(' please correct the time before AM !'), '+'),Js(1.0).neg())
                PyJsComma(var.put('z', var.get('RegExp').create(var.get('q').get('clockTime').get('regexexec').get('4'), Js('ig'))),(var.get('z').callprop('test', var.get('w')) and PyJsComma(var.put('A', var.get('w').callprop('match', var.get('z'))),(PyJsComma(var.put('B', Js(12.0)),var.put('C', Js(0.0))) if (Js('noon')==var.get('A')) else PyJsComma(var.put('B', Js(0.0)),var.put('C', Js(0.0)))))))
                var.put('F', var.get('x').get((var.get('x').get('length')-Js(1.0))))
                if (var.get(u"null")!=var.get('F')):
                    if ((Js(0.0).neg()==var.get('s').get('isRangeForHour')) or (Js(0.0).neg()==var.get('s').get('isRangeForMin'))):
                        return PyJsComma(var.put('y', Js(' already set for range expressions, seperate into two crons!'), '+'),Js(1.0).neg())
                    if (Js('rangeStart')==var.get('F').get('ownerState')):
                        return PyJsComma(PyJsComma(PyJsComma(PyJsComma(var.get('F').get('hour').put('start', var.get('B')),var.get('F').get('min').put('start', var.get('C'))),var.get('x').callprop('pop')),var.get('x').callprop('push', var.get('F'))),Js(0.0).neg())
                    if (Js('rangeEnd')==var.get('F').get('ownerState')):
                        def PyJs_LONG_12_(var=var):
                            return (PyJsComma(PyJsComma(var.get('F').get('min').put('end', var.get('C')),var.get('v').put('min', ((var.get('F').get('min').get('start')+Js('-'))+var.get('F').get('min').get('end')))),Js(0.0).neg()) if (var.get('F').get('hour')==var.get('B')) else PyJsComma(PyJsComma(var.get('F').get('hour').put('end', var.get('B')),var.get('v').put('hour', ((var.get('F').get('hour').get('start')+Js('-'))+var.get('F').get('hour').get('end')))),Js(0.0).neg()))
                        return PyJs_LONG_12_()
                var.put('G', Js({'ownerState':Js('clockTime'),'hour':var.get('B'),'min':var.get('C')}))
                return PyJsComma(PyJsComma(PyJsComma(var.get('v').put('min', var.get('C')),(var.get('v').put('hour', (Js(',')+var.get('B')), '+') if ((Js('*')!=var.get('v').get('hour')) and (Js('')!=var.get('v').get('hour'))) else var.get('v').put('hour', var.get('B')))),var.get('x').callprop('push', var.get('G'))),Js(0.0).neg())
            PyJs_anonymous_10_._set_name('anonymous')
            var.get('k').put('exports', Js({'getClockTime':PyJs_anonymous_10_}))
        PyJs_anonymous_9_._set_name('anonymous')
        @Js
        def PyJs_anonymous_13_(j, k, this, arguments, var=var):
            var = Scope({'j':j, 'k':k, 'this':this, 'arguments':arguments}, var)
            var.registers(['v', 'j', 'q', 's', 'k'])
            Js('use strict')
            var.put('q', var.get('j')(Js('../maps')).get('regexString'))
            var.put('s', var.get('j')(Js('../maps')).get('flags'))
            var.put('v', var.get('j')(Js('../maps')).get('resultCron'))
            @Js
            def PyJs_anonymous_14_(w, x, y, this, arguments, var=var):
                var = Scope({'w':w, 'x':x, 'y':y, 'this':this, 'arguments':arguments}, var)
                var.registers(['D', 'C', 'w', 'x', 'B', 'A', 'y', 'z', 'E'])
                var.put('z', var.get('RegExp').create(var.get('q').get('day').get('regexexec').get('0'), Js('ig')))
                var.put('A', Js(''))
                if var.get('z').callprop('test', var.get('w')):
                    var.put('C', var.get('x').get((var.get('x').get('length')-Js(1.0))))
                    def PyJs_LONG_15_(var=var):
                        return (var.put('C', Js({'frequency':Js('*')})) if (var.get(u"null")==var.get('C')) else (PyJsComma(var.get('v').put('day_of_month', (Js('0/')+var.get('C').get('frequency'))),var.get('x').callprop('pop')) if (Js('frequencyOnly')==var.get('C').get('ownerState')) else (PyJsComma(var.get('v').put('day_of_month', (Js('')+var.get('C').get('frequency'))),var.get('x').callprop('pop')) if (Js('frequencyWith')==var.get('C').get('ownerState')) else var.get('v').put('day_of_month', Js('*')))))
                    PyJsComma(var.get('v').put('day_of_week', Js('?')),PyJs_LONG_15_())
                else:
                    var.put('z', var.get('RegExp').create(var.get('q').get('day').get('regexexec').get('1'), Js('ig')))
                    var.put('C', var.get('w').callprop('match', var.get('z')))
                    if ((var.get(u"null")!=var.get('C')) and (Js(0.0)!=var.get('C').get('length'))):
                        var.get('v').put('day_of_week', Js(''))
                        #for JS loop
                        var.put('E', Js(0.0))
                        while (var.get('E')<var.get('C').get('length')):
                            try:
                                var.get('C').put(var.get('E'), var.get('C').get(var.get('E')).callprop('toUpperCase'))
                            finally:
                                    (var.put('E',Js(var.get('E').to_number())+Js(1))-Js(1))
                        var.put('D', var.get('x').get((var.get('x').get('length')-Js(1.0))))
                        if ((Js(1.0)==var.get('C').get('length')) and (var.get(u"null")!=var.get('D'))):
                            if (Js(0.0).neg()==var.get('s').get('isRangeForDay')):
                                return PyJsComma(var.put('y', Js(' already set for range expressions, seperate into two crons!'), '+'),Js(1.0).neg())
                            if PyJsComma(var.get('x').callprop('pop'),(Js('rangeStart')==var.get('D').get('ownerState'))):
                                return PyJsComma(PyJsComma(var.get('D').get('day').put('start', var.get('C').get('0')),var.get('x').callprop('push', var.get('D'))),Js(0.0).neg())
                            if (Js('rangeEnd')==var.get('D').get('ownerState')):
                                return PyJsComma(PyJsComma(PyJsComma(var.get('D').get('day').put('end', var.get('C').get('0')),var.get('v').put('day_of_week', ((var.get('D').get('day').get('start')+Js('-'))+var.get('D').get('day').get('end')))),var.get('v').put('day_of_month', Js('?'))),Js(0.0).neg())
                        def PyJs_LONG_16_(var=var):
                            return PyJsComma(PyJsComma(PyJsComma(PyJsComma(PyJsComma(PyJsComma(PyJsComma(PyJsComma(PyJsComma(PyJsComma(PyJsComma(((var.get('C').callprop('includes', Js('MON')) and var.get('v').get('day_of_week').callprop('includes', Js('MON')).neg()) and var.get('v').put('day_of_week', Js('MON,'), '+')),((var.get('C').callprop('includes', Js('TUE')) and var.get('v').get('day_of_week').callprop('includes', Js('TUE')).neg()) and var.get('v').put('day_of_week', Js('TUE,'), '+'))),((var.get('C').callprop('includes', Js('WED')) and var.get('v').get('day_of_week').callprop('includes', Js('WED')).neg()) and var.get('v').put('day_of_week', Js('WED,'), '+'))),((var.get('C').callprop('includes', Js('THU')) and var.get('v').get('day_of_week').callprop('includes', Js('THU')).neg()) and var.get('v').put('day_of_week', Js('THU,'), '+'))),((var.get('C').callprop('includes', Js('FRI')) and var.get('v').get('day_of_week').callprop('includes', Js('FRI')).neg()) and var.get('v').put('day_of_week', Js('FRI,'), '+'))),((var.get('C').callprop('includes', Js('SAT')) and var.get('v').get('day_of_week').callprop('includes', Js('SAT')).neg()) and var.get('v').put('day_of_week', Js('SAT,'), '+'))),((var.get('C').callprop('includes', Js('SUN')) and var.get('v').get('day_of_week').callprop('includes', Js('SUN')).neg()) and var.get('v').put('day_of_week', Js('SUN,'), '+'))),((var.get('C').callprop('includes', Js('WEEKEND')) and var.get('v').get('day_of_week').callprop('includes', Js('SAT')).neg()) and var.get('v').put('day_of_week', Js('SAT,'), '+'))),((var.get('C').callprop('includes', Js('WEEKEND')) and var.get('v').get('day_of_week').callprop('includes', Js('SUN')).neg()) and var.get('v').put('day_of_week', Js('SUN,'), '+'))),var.get('v').put('day_of_week', var.get('v').get('day_of_week').callprop('slice', Js(0.0), (-Js(1.0))))),var.get('v').put('day_of_month', Js('?'))),var.put('A', (Js('')+var.get('v').get('day_of_week'))))
                        PyJs_LONG_16_()
                    else:
                        return PyJsComma(var.put('y', Js(' In unresolved state at 2;Day !'), '+'),Js(1.0).neg())
                var.put('B', Js({'ownerState':Js('day'),'day_of_week':var.get('v').get('day_of_week'),'day_of_month':var.get('v').get('day_of_month')}))
                return PyJsComma(var.get('x').callprop('push', var.get('B')),Js(0.0).neg())
            PyJs_anonymous_14_._set_name('anonymous')
            var.get('k').put('exports', Js({'getDay':PyJs_anonymous_14_}))
        PyJs_anonymous_13_._set_name('anonymous')
        @Js
        def PyJs_anonymous_17_(j, k, this, arguments, var=var):
            var = Scope({'j':j, 'k':k, 'this':this, 'arguments':arguments}, var)
            var.registers(['v', 'j', 'w', 's', 'k'])
            Js('use strict')
            var.put('s', var.get('j')(Js('../maps')).get('regexString'))
            var.put('v', var.get('j')(Js('../maps')).get('flags'))
            var.put('w', var.get('j')(Js('../maps')).get('resultCron'))
            @Js
            def PyJs_anonymous_18_(x, y, z, this, arguments, var=var):
                var = Scope({'x':x, 'y':y, 'z':z, 'this':this, 'arguments':arguments}, var)
                var.registers(['C', 'x', 'A', 'y', 'z'])
                var.put('A', var.get('parseInt')(var.get('x')))
                if var.get('isNaN')(var.get('x')):
                    return PyJsComma(var.put('z', Js(' token is not number in frequency only !'), '+'),Js(1.0).neg())
                if ((Js(0.0)<var.get('y').get('length')) and (Js('rangeEnd')==var.get('y').get((var.get('y').get('length')-Js(1.0))).get('ownerState'))):
                    var.put('C', var.get('y').get((var.get('y').get('length')-Js(1.0))))
                    return PyJsComma(PyJsComma(PyJsComma(var.get('y').callprop('pop'),var.get('C').get('frequency').put('end', var.get('A'))),var.get('y').callprop('push', var.get('C'))),Js(0.0).neg())
                if ((Js(0.0)<var.get('y').get('length')) and (Js('rangeStart')==var.get('y').get((var.get('y').get('length')-Js(1.0))).get('ownerState'))):
                    var.put('C', var.get('y').get((var.get('y').get('length')-Js(1.0))))
                    return PyJsComma(PyJsComma(PyJsComma(var.get('y').callprop('pop'),var.get('C').get('frequency').put('start', var.get('A'))),var.get('y').callprop('push', var.get('C'))),Js(0.0).neg())
                return PyJsComma(var.get('y').callprop('push', Js({'ownerState':Js('frequencyOnly'),'frequency':var.get('A')})),Js(0.0).neg())
            PyJs_anonymous_18_._set_name('anonymous')
            @Js
            def PyJs_anonymous_19_(x, y, z, this, arguments, var=var):
                var = Scope({'x':x, 'y':y, 'z':z, 'this':this, 'arguments':arguments}, var)
                var.registers(['C', 'x', 'B', 'A', 'y', 'z', 'E'])
                var.put('A', var.get('RegExp').create(var.get('s').get('frequencyOnly').get('regexexec'), Js('ig')))
                var.put('B', var.get('A').callprop('exec', var.get('x')))
                var.put('C', var.get('parseInt')(var.get('B')))
                if var.get('isNaN')(var.get('C')):
                    return PyJsComma(var.put('z', Js(' token is not number in frequency with !'), '+'),Js(1.0).neg())
                if ((Js(0.0)!=var.get('y').get('length')) and (Js('rangeEnd')==var.get('y').get((var.get('y').get('length')-Js(1.0))).get('ownerState'))):
                    var.put('E', var.get('y').get((var.get('y').get('length')-Js(1.0))))
                    return PyJsComma(PyJsComma(PyJsComma(var.get('y').callprop('pop'),var.get('E').get('frequency').put('end', (Js('')+var.get('C')))),var.get('y').callprop('push', var.get('E'))),Js(0.0).neg())
                if ((Js(0.0)<var.get('y').get('length')) and (Js('rangeStart')==var.get('y').get((var.get('y').get('length')-Js(1.0))).get('ownerState'))):
                    var.put('E', var.get('y').get((var.get('y').get('length')-Js(1.0))))
                    return PyJsComma(PyJsComma(PyJsComma(var.get('y').callprop('pop'),var.get('E').get('frequency').put('start', (Js('')+var.get('C')))),var.get('y').callprop('push', var.get('E'))),Js(0.0).neg())
                return PyJsComma(var.get('y').callprop('push', Js({'ownerState':Js('frequencyWith'),'frequency':var.get('C')})),Js(0.0).neg())
            PyJs_anonymous_19_._set_name('anonymous')
            var.get('k').put('exports', Js({'getFrequencyOnly':PyJs_anonymous_18_,'getFrequencyWith':PyJs_anonymous_19_}))
        PyJs_anonymous_17_._set_name('anonymous')
        @Js
        def PyJs_anonymous_20_(j, k, this, arguments, var=var):
            var = Scope({'j':j, 'k':k, 'this':this, 'arguments':arguments}, var)
            var.registers(['v', 'j', 'q', 's', 'k'])
            Js('use strict')
            var.put('q', var.get('j')(Js('../maps')).get('regexString'))
            var.put('s', var.get('j')(Js('../maps')).get('flags'))
            var.put('v', var.get('j')(Js('../maps')).get('resultCron'))
            @Js
            def PyJs_anonymous_21_(w, x, y, this, arguments, var=var):
                var = Scope({'w':w, 'x':x, 'y':y, 'this':this, 'arguments':arguments}, var)
                var.registers(['C', 'w', 'x', 'B', 'A', 'y', 'z'])
                var.put('z', var.get('RegExp').create(var.get('q').get('hour').get('regexexec').get('0'), Js('ig')))
                if var.get('z').callprop('test', var.get('w')):
                    var.put('C', var.get('x').get((var.get('x').get('length')-Js(1.0))))
                    if (var.get(u"null")==var.get('C')):
                        var.put('C', Js({'frequency':Js('*')}))
                    else:
                        if (Js('frequencyOnly')==var.get('C').get('ownerState')):
                            PyJsComma(PyJsComma(var.put('A', var.get('C').get('frequency')),var.get('v').put('hour', (Js('0/')+var.get('C').get('frequency')))),var.get('x').callprop('pop'))
                        else:
                            if (Js('frequencyWith')==var.get('C').get('ownerState')):
                                PyJsComma(PyJsComma((var.get('v').put('hour', (Js(',')+var.get('C').get('frequency')), '+') if ((Js('*')!=var.get('v').get('hour')) and (Js('')!=var.get('v').get('hour'))) else var.get('v').put('hour', (Js('')+var.get('C').get('frequency')))),var.put('A', var.get('v').get('hour'))),var.get('x').callprop('pop'))
                            else:
                                if (Js(0.0).neg()==var.get('s').get('isRangeForHour')):
                                    return PyJsComma(var.put('y', Js(' already set for range expressions, seperate into two crons!'), '+'),Js(1.0).neg())
                                if (Js('rangeStart')==var.get('C').get('ownerState')):
                                    return PyJsComma(PyJsComma(PyJsComma(PyJsComma(var.get('C').get('hour').put('start', var.get('C').get('frequency').get('start')),var.get('C').get('frequency').put('start', Js(''))),var.get('x').callprop('pop')),var.get('x').callprop('push', var.get('C'))),Js(0.0).neg())
                                if (Js('rangeEnd')==var.get('C').get('ownerState')):
                                    def PyJs_LONG_22_(var=var):
                                        return PyJsComma(PyJsComma(PyJsComma(PyJsComma(PyJsComma(var.get('x').callprop('pop'),var.get('C').get('hour').put('start', var.get('C').get('frequency').get('start'))),var.get('C').get('hour').put('end', var.get('C').get('frequency').get('end'))),var.get('C').get('frequency').put('end', Js(''))),var.get('v').put('hour', ((var.get('C').get('hour').get('start')+Js('-'))+var.get('C').get('hour').get('end')))),Js(0.0).neg())
                                    return PyJs_LONG_22_()
                var.put('B', Js({'ownerState':Js('hour'),'hour':var.get('A')}))
                return PyJsComma(var.get('x').callprop('push', var.get('B')),Js(0.0).neg())
            PyJs_anonymous_21_._set_name('anonymous')
            var.get('k').put('exports', Js({'getHour':PyJs_anonymous_21_}))
        PyJs_anonymous_20_._set_name('anonymous')
        @Js
        def PyJs_anonymous_23_(j, k, this, arguments, var=var):
            var = Scope({'j':j, 'k':k, 'this':this, 'arguments':arguments}, var)
            var.registers(['v', 'j', 'q', 's', 'k'])
            Js('use strict')
            var.put('q', var.get('j')(Js('../maps')).get('regexString'))
            var.put('s', var.get('j')(Js('../maps')).get('flags'))
            var.put('v', var.get('j')(Js('../maps')).get('resultCron'))
            @Js
            def PyJs_anonymous_24_(w, x, y, this, arguments, var=var):
                var = Scope({'w':w, 'x':x, 'y':y, 'this':this, 'arguments':arguments}, var)
                var.registers(['C', 'w', 'x', 'B', 'A', 'y', 'z'])
                var.put('z', var.get('RegExp').create(var.get('q').get('minute').get('regexexec').get('0'), Js('ig')))
                if var.get('z').callprop('test', var.get('w')):
                    var.put('C', var.get('x').get((var.get('x').get('length')-Js(1.0))))
                    if (var.get(u"null")==var.get('C')):
                        var.put('C', Js({'frequency':Js('*')}))
                    else:
                        if (Js('frequencyOnly')==var.get('C').get('ownerState')):
                            PyJsComma(PyJsComma(var.put('A', var.get('C').get('frequency')),var.get('v').put('min', (Js('0/')+var.get('C').get('frequency')))),var.get('x').callprop('pop'))
                        else:
                            if (Js('frequencyWith')==var.get('C').get('ownerState')):
                                PyJsComma(PyJsComma(var.put('A', var.get('C').get('frequency')),var.get('v').put('min', (Js('')+var.get('C').get('frequency')))),var.get('x').callprop('pop'))
                            else:
                                if (Js(0.0).neg()==var.get('s').get('isRangeForMinute')):
                                    return PyJsComma(var.put('y', Js(' already set for range expressions, seperate into two crons!'), '+'),Js(1.0).neg())
                                if (Js('rangeStart')==var.get('C').get('ownerState')):
                                    return PyJsComma(PyJsComma(PyJsComma(PyJsComma(var.get('C').get('min').put('start', var.get('C').get('frequency').get('start')),var.get('C').get('frequency').put('start', Js(''))),var.get('x').callprop('pop')),var.get('x').callprop('push', var.get('C'))),Js(0.0).neg())
                                if (Js('rangeEnd')==var.get('C').get('ownerState')):
                                    def PyJs_LONG_25_(var=var):
                                        return PyJsComma(PyJsComma(PyJsComma(PyJsComma(PyJsComma(var.get('x').callprop('pop'),var.get('C').get('min').put('start', var.get('C').get('frequency').get('start'))),var.get('C').get('min').put('end', var.get('C').get('frequency').get('end'))),var.get('C').get('frequency').put('end', Js(''))),var.get('v').put('min', ((var.get('C').get('min').get('start')+Js('-'))+var.get('C').get('min').get('end')))),Js(0.0).neg())
                                    return PyJs_LONG_25_()
                var.put('B', Js({'ownerState':Js('minute'),'min':var.get('A')}))
                return PyJsComma(var.get('x').callprop('push', var.get('B')),Js(0.0).neg())
            PyJs_anonymous_24_._set_name('anonymous')
            var.get('k').put('exports', Js({'getMinute':PyJs_anonymous_24_}))
        PyJs_anonymous_23_._set_name('anonymous')
        @Js
        def PyJs_anonymous_26_(j, k, this, arguments, var=var):
            var = Scope({'j':j, 'k':k, 'this':this, 'arguments':arguments}, var)
            var.registers(['v', 'j', 'q', 's', 'k'])
            Js('use strict')
            var.put('q', var.get('j')(Js('../maps')).get('regexString'))
            var.put('s', var.get('j')(Js('../maps')).get('flags'))
            var.put('v', var.get('j')(Js('../maps')).get('resultCron'))
            @Js
            def PyJs_anonymous_27_(w, x, y, this, arguments, var=var):
                var = Scope({'w':w, 'x':x, 'y':y, 'this':this, 'arguments':arguments}, var)
                var.registers(['D', 'C', 'w', 'x', 'B', 'A', 'y', 'z', 'E'])
                var.put('z', var.get('RegExp').create(var.get('q').get('month').get('regexexec').get('0'), Js('ig')))
                var.put('A', Js(''))
                if var.get('z').callprop('test', var.get('w')):
                    var.put('C', var.get('x').get((var.get('x').get('length')-Js(1.0))))
                    def PyJs_LONG_28_(var=var):
                        return PyJsComma(((var.get(u"null")==var.get('C')) and var.put('C', Js({'frequency':Js('*')}))),(PyJsComma(var.get('v').put('month', (Js('0/')+var.get('C').get('frequency'))),var.get('x').callprop('pop')) if (Js('frequencyOnly')==var.get('C').get('ownerState')) else (PyJsComma(var.get('v').put('month', (Js('')+var.get('C').get('frequency'))),var.get('x').callprop('pop')) if (Js('frequencyWith')==var.get('C').get('ownerState')) else var.get('v').put('month', Js('*')))))
                    PyJs_LONG_28_()
                else:
                    var.put('z', var.get('RegExp').create(var.get('q').get('month').get('regexexec').get('1'), Js('ig')))
                    var.put('C', var.get('w').callprop('match', var.get('z')))
                    if ((var.get(u"null")!=var.get('C')) and (Js(0.0)!=var.get('C').get('length'))):
                        var.get('v').put('month', Js(''))
                        #for JS loop
                        var.put('E', Js(0.0))
                        while (var.get('E')<var.get('C').get('length')):
                            try:
                                var.get('C').put(var.get('E'), var.get('C').get(var.get('E')).callprop('toUpperCase'))
                            finally:
                                    (var.put('E',Js(var.get('E').to_number())+Js(1))-Js(1))
                        var.put('D', var.get('x').get((var.get('x').get('length')-Js(1.0))))
                        if ((Js(1.0)==var.get('C').get('length')) and (var.get(u"null")!=var.get('D'))):
                            if (Js(0.0).neg()==var.get('s').get('isRangeForMonth')):
                                return PyJsComma(var.put('y', Js(' already set for range expressions, seperate into two crons!'), '+'),Js(1.0).neg())
                            if PyJsComma(var.get('x').callprop('pop'),(Js('frequencyOnly')==var.get('D').get('ownerState'))):
                                var.get('v').put('day_of_month', var.get('D').get('frequency'))
                            else:
                                if (Js('frequencyWith')==var.get('D').get('ownerState')):
                                    var.get('v').put('day_of_month', var.get('D').get('frequency'))
                                else:
                                    if (Js('rangeStart')==var.get('D').get('ownerState')):
                                        return PyJsComma(PyJsComma(var.get('D').get('month').put('start', var.get('C').get('0')),var.get('x').callprop('push', var.get('D'))),Js(0.0).neg())
                                    if (Js('rangeEnd')==var.get('D').get('ownerState')):
                                        def PyJs_LONG_29_(var=var):
                                            return PyJsComma(PyJsComma(PyJsComma(((Js('')!=var.get('D').get('frequency').get('end')) and PyJsComma(var.get('v').put('day_of_week', Js('?')),var.get('v').put('day_of_month', ((var.get('D').get('frequency').get('start')+Js('-'))+var.get('D').get('frequency').get('end'))))),var.get('D').get('month').put('end', var.get('C').get('0'))),var.get('v').put('month', ((var.get('D').get('month').get('start')+Js('-'))+var.get('D').get('month').get('end')))),Js(0.0).neg())
                                        return PyJs_LONG_29_()
                        def PyJs_LONG_30_(var=var):
                            return PyJsComma(PyJsComma(PyJsComma(PyJsComma(PyJsComma(PyJsComma(PyJsComma(PyJsComma(PyJsComma(PyJsComma(PyJsComma(PyJsComma(PyJsComma(((var.get('C').callprop('includes', Js('JAN')) and var.get('v').get('month').callprop('includes', Js('JAN')).neg()) and var.get('v').put('month', Js('JAN,'), '+')),((var.get('C').callprop('includes', Js('FEB')) and var.get('v').get('month').callprop('includes', Js('FEB')).neg()) and var.get('v').put('month', Js('FEB,'), '+'))),((var.get('C').callprop('includes', Js('MAR')) and var.get('v').get('month').callprop('includes', Js('MAR')).neg()) and var.get('v').put('month', Js('MAR,'), '+'))),((var.get('C').callprop('includes', Js('APR')) and var.get('v').get('month').callprop('includes', Js('APR')).neg()) and var.get('v').put('month', Js('APR,'), '+'))),((var.get('C').callprop('includes', Js('MAY')) and var.get('v').get('month').callprop('includes', Js('MAY')).neg()) and var.get('v').put('month', Js('MAY,'), '+'))),((var.get('C').callprop('includes', Js('JUN')) and var.get('v').get('month').callprop('includes', Js('JUN')).neg()) and var.get('v').put('month', Js('JUN,'), '+'))),((var.get('C').callprop('includes', Js('JUL')) and var.get('v').get('month').callprop('includes', Js('JUL')).neg()) and var.get('v').put('month', Js('JUL,'), '+'))),((var.get('C').callprop('includes', Js('AUG')) and var.get('v').get('month').callprop('includes', Js('AUG')).neg()) and var.get('v').put('month', Js('AUG,'), '+'))),((var.get('C').callprop('includes', Js('SEPT')) and var.get('v').get('month').callprop('includes', Js('SEPT')).neg()) and var.get('v').put('month', Js('SEPT,'), '+'))),((var.get('C').callprop('includes', Js('OCT')) and var.get('v').get('month').callprop('includes', Js('OCT')).neg()) and var.get('v').put('month', Js('OCT,'), '+'))),((var.get('C').callprop('includes', Js('NOV')) and var.get('v').get('month').callprop('includes', Js('NOV')).neg()) and var.get('v').put('month', Js('NOV,'), '+'))),((var.get('C').callprop('includes', Js('DEC')) and var.get('v').get('month').callprop('includes', Js('DEC')).neg()) and var.get('v').put('month', Js('DEC,'), '+'))),var.get('v').put('month', var.get('v').get('month').callprop('slice', Js(0.0), (-Js(1.0))))),var.put('A', (Js('')+var.get('v').get('month'))))
                        PyJs_LONG_30_()
                    else:
                        return PyJsComma(var.put('y', Js(' In unresolved state at 2;Month !'), '+'),Js(1.0).neg())
                var.put('B', Js({'ownerState':Js('month'),'month':var.get('v').get('month')}))
                return PyJsComma(var.get('x').callprop('push', var.get('B')),Js(0.0).neg())
            PyJs_anonymous_27_._set_name('anonymous')
            var.get('k').put('exports', Js({'getMonth':PyJs_anonymous_27_}))
        PyJs_anonymous_26_._set_name('anonymous')
        @Js
        def PyJs_anonymous_31_(j, k, this, arguments, var=var):
            var = Scope({'j':j, 'k':k, 'this':this, 'arguments':arguments}, var)
            var.registers(['w', 'v', 'k', 'j'])
            Js('use strict')
            var.get('j')(Js('../maps')).get('regexString')
            var.put('v', var.get('j')(Js('../maps')).get('flags'))
            var.put('w', var.get('j')(Js('../maps')).get('resultCron'))
            @Js
            def PyJs_anonymous_32_(x, y, z, this, arguments, var=var):
                var = Scope({'x':x, 'y':y, 'z':z, 'this':this, 'arguments':arguments}, var)
                var.registers(['x', 'y', 'z'])
                if ((((var.get('v').get('isRangeForDay') or var.get('v').get('isRangeForMin')) or var.get('v').get('isRangeForMonth')) or var.get('v').get('isRangeForYear')) or var.get('v').get('isRangeForHour')):
                    return PyJsComma(var.put('z', Js(' already range expressions !'), '+'),Js(1.0).neg())
                return PyJsComma(var.get('y').callprop('push', Js({'ownerState':Js('rangeStart'),'min':Js({'start':Js(''),'end':Js('')}),'hour':Js({'start':Js(''),'end':Js('')}),'day':Js({'start':Js(''),'end':Js('')}),'month':Js({'start':Js(''),'end':Js('')}),'year':Js({'start':Js(''),'end':Js('')}),'frequency':Js({'start':Js(''),'end':Js('')})})),Js(0.0).neg())
            PyJs_anonymous_32_._set_name('anonymous')
            @Js
            def PyJs_anonymous_33_(x, y, this, arguments, var=var):
                var = Scope({'x':x, 'y':y, 'this':this, 'arguments':arguments}, var)
                var.registers(['A', 'y', 'x', 'B'])
                var.put('A', Js({'ownerState':Js('rangeEnd'),'min':Js({'start':Js(''),'end':Js('')}),'hour':Js({'start':Js(''),'end':Js('')}),'day':Js({'start':Js(''),'end':Js('')}),'month':Js({'start':Js(''),'end':Js('')}),'year':Js({'start':Js(''),'end':Js('')}),'frequency':Js({'start':Js(''),'end':Js('')})}))
                var.put('B', var.get('y').get((var.get('y').get('length')-Js(1.0))))
                if (var.get(u"null")!=var.get('B')):
                    while 1:
                        SWITCHED = False
                        CONDITION = (var.get('B').get('ownerState'))
                        if SWITCHED or PyJsStrictEq(CONDITION, Js('frequencyWith')):
                            SWITCHED = True
                            pass
                        if SWITCHED or PyJsStrictEq(CONDITION, Js('frequencyOnly')):
                            SWITCHED = True
                            PyJsComma(PyJsComma(PyJsComma(var.get('y').callprop('pop'),var.get('A').get('frequency').put('start', var.get('B').get('frequency'))),var.get('A').put('ownerState', Js('rangeEnd'))),var.get('y').callprop('push', var.get('A')))
                            break
                        if SWITCHED or PyJsStrictEq(CONDITION, Js('clockTime')):
                            SWITCHED = True
                            PyJsComma(PyJsComma(PyJsComma(PyJsComma(var.get('y').callprop('pop'),var.get('A').get('hour').put('start', var.get('B').get('hour'))),var.get('A').get('min').put('start', var.get('B').get('min'))),var.get('A').put('ownerState', Js('rangeEnd'))),var.get('y').callprop('push', var.get('A')))
                            break
                        if SWITCHED or PyJsStrictEq(CONDITION, Js('rangeStart')):
                            SWITCHED = True
                            PyJsComma(PyJsComma(var.get('y').callprop('pop'),var.get('B').put('ownerState', Js('rangeEnd'))),var.get('y').callprop('push', var.get('B')))
                            break
                        if SWITCHED or PyJsStrictEq(CONDITION, Js('month')):
                            SWITCHED = True
                            PyJsComma(PyJsComma(PyJsComma(var.get('y').callprop('pop'),var.get('A').put('ownerState', Js('rangeEnd'))),var.get('A').get('month').put('start', var.get('B').get('month'))),var.get('y').callprop('push', var.get('A')))
                            break
                        if SWITCHED or PyJsStrictEq(CONDITION, Js('minute')):
                            SWITCHED = True
                            PyJsComma(PyJsComma(PyJsComma(var.get('y').callprop('pop'),var.get('A').put('ownerState', Js('rangeEnd'))),var.get('A').get('frequency').put('start', var.get('A').get('min').put('start', var.get('B').get('min')))),var.get('y').callprop('push', var.get('A')))
                            break
                        if SWITCHED or PyJsStrictEq(CONDITION, Js('hour')):
                            SWITCHED = True
                            PyJsComma(PyJsComma(PyJsComma(var.get('y').callprop('pop'),var.get('A').put('ownerState', Js('rangeEnd'))),var.get('A').get('frequency').put('start', var.get('A').get('hour').put('start', var.get('B').get('hour')))),var.get('y').callprop('push', var.get('A')))
                            break
                        if SWITCHED or PyJsStrictEq(CONDITION, Js('day')):
                            SWITCHED = True
                            PyJsComma(PyJsComma(PyJsComma(var.get('y').callprop('pop'),var.get('A').put('ownerState', Js('rangeEnd'))),var.get('A').get('day').put('start', var.get('B').get('day_of_week'))),var.get('y').callprop('push', var.get('A')))
                            break
                        if SWITCHED or PyJsStrictEq(CONDITION, Js('year')):
                            SWITCHED = True
                            PyJsComma(PyJsComma(PyJsComma(var.get('y').callprop('pop'),var.get('A').put('ownerState', Js('rangeEnd'))),var.get('A').get('year').put('start', var.get('B').get('year'))),var.get('y').callprop('push', var.get('A')))
                        SWITCHED = True
                        break
                return Js(0.0).neg()
            PyJs_anonymous_33_._set_name('anonymous')
            var.get('k').put('exports', Js({'rangeStartState':PyJs_anonymous_32_,'rangeEndState':PyJs_anonymous_33_}))
        PyJs_anonymous_31_._set_name('anonymous')
        @Js
        def PyJs_anonymous_34_(j, k, this, arguments, var=var):
            var = Scope({'j':j, 'k':k, 'this':this, 'arguments':arguments}, var)
            var.registers(['v', 'j', 'q', 's', 'k'])
            Js('use strict')
            var.put('q', var.get('j')(Js('../maps')).get('regexString'))
            var.put('s', var.get('j')(Js('../maps')).get('flags'))
            var.put('v', var.get('j')(Js('../maps')).get('resultCron'))
            @Js
            def PyJs_anonymous_35_(w, x, y, this, arguments, var=var):
                var = Scope({'w':w, 'x':x, 'y':y, 'this':this, 'arguments':arguments}, var)
                var.registers(['D', 'G', 'F', 'C', 'w', 'x', 'B', 'A', 'y', 'z', 'E'])
                var.put('z', var.get('RegExp').create(var.get('q').get('year').get('regexexec').get('0'), Js('ig')))
                var.put('A', Js(''))
                if var.get('z').callprop('test', var.get('w')):
                    var.put('C', var.get('x').get((var.get('x').get('length')-Js(1.0))))
                    def PyJs_LONG_36_(var=var):
                        return (var.put('C', Js({'frequency':Js('*')})) if (var.get(u"null")==var.get('C')) else (PyJsComma(var.get('v').put('year', (Js('0/')+var.get('C').get('frequency'))),var.get('x').callprop('pop')) if (Js('frequencyOnly')==var.get('C').get('ownerState')) else (PyJsComma(var.get('v').put('year', (Js('')+var.get('C').get('frequency'))),var.get('x').callprop('pop')) if (Js('frequencyWith')==var.get('C').get('ownerState')) else var.get('v').put('year', Js('*')))))
                    PyJsComma(var.get('v').put('year', Js('?')),PyJs_LONG_36_())
                else:
                    var.put('z', var.get('RegExp').create(var.get('q').get('year').get('regexexec').get('1'), Js('ig')))
                    var.put('C', var.get('RegExp').create(var.get('q').get('year').get('regexexec').get('2'), Js('ig')))
                    var.put('D', var.get('w').callprop('match', var.get('z')))
                    var.put('E', var.get('Set').create())
                    #for JS loop
                    var.put('G', Js(0.0))
                    while (var.get('G')<var.get('D').get('length')):
                        try:
                            (var.get('C').callprop('test', var.get('D').get(var.get('G'))) and var.get('E').callprop('add', var.get('D').get(var.get('G')).callprop('match', var.get('C')).get('0')))
                        finally:
                                (var.put('G',Js(var.get('G').to_number())+Js(1))-Js(1))
                    var.put('F', var.get('x').get((var.get('x').get('length')-Js(1.0))))
                    if ((Js(1.0)==var.get('E').get('size')) and (var.get(u"null")!=var.get('F'))):
                        if (Js(0.0).neg()==var.get('s').get('isRangeForYear')):
                            return PyJsComma(var.put('y', Js(' Cannot handle multiple range expressions, seperate into two crons!'), '+'),Js(1.0).neg())
                        if (Js('rangeStart')==var.get('F').get('ownerState')):
                            return PyJsComma(PyJsComma(PyJsComma(var.get('F').get('year').put('start', var.get('Array').callprop('from', var.get('E')).get('0')),var.get('x').callprop('pop')),var.get('x').callprop('push', var.get('F'))),Js(0.0).neg())
                        if (Js('rangeEnd')==var.get('F').get('ownerState')):
                            return PyJsComma(PyJsComma(PyJsComma(var.get('F').get('year').put('end', var.get('Array').callprop('from', var.get('E')).get('0')),var.get('x').callprop('pop')),var.get('v').put('year', ((var.get('F').get('year').get('start')+Js('-'))+var.get('F').get('year').get('end')))),Js(0.0).neg())
                    if (Js(0.0)!=var.get('E').get('size')):
                        @Js
                        def PyJs_anonymous_37_(G, this, arguments, var=var):
                            var = Scope({'G':G, 'this':this, 'arguments':arguments}, var)
                            var.registers(['G'])
                            var.get('v').put('year', (var.get('G')+Js(',')), '+')
                        PyJs_anonymous_37_._set_name('anonymous')
                        PyJsComma(PyJsComma(PyJsComma(var.get('v').put('year', Js('')),var.get('E').callprop('forEach', PyJs_anonymous_37_)),var.get('v').put('year', var.get('v').get('year').callprop('slice', Js(0.0), (-Js(1.0))))),var.put('A', (Js('')+var.get('v').get('year'))))
                    else:
                        return PyJsComma(var.put('y', Js(' In unresolved state at 2;year !'), '+'),Js(1.0).neg())
                var.put('B', Js({'ownerState':Js('year'),'year':var.get('v').get('year')}))
                return PyJsComma(var.get('x').callprop('push', var.get('B')),Js(0.0).neg())
            PyJs_anonymous_35_._set_name('anonymous')
            var.get('k').put('exports', Js({'getYear':PyJs_anonymous_35_}))
        PyJs_anonymous_34_._set_name('anonymous')
        @Js
        def PyJs_anonymous_38_(j, k, this, arguments, var=var):
            var = Scope({'j':j, 'k':k, 'this':this, 'arguments':arguments}, var)
            var.registers(['j', 'q', 's', 'm', 'k'])
            Js('use strict')
            var.put('m', var.get('j')(Js('./maps')).get('regexString'))
            var.put('q', var.get('j')(Js('./maps')).get('flags'))
            var.put('s', var.get('j')(Js('./maps')).get('resultCron'))
            @Js
            def PyJs_anonymous_39_(v, this, arguments, var=var):
                var = Scope({'v':v, 'this':this, 'arguments':arguments}, var)
                var.registers(['x', 'w', 'v', 'y'])
                var.put('w', var.get('RegExp').create(var.get('m').get('tokenising').get('regexexec'), Js('ig')))
                var.put('x', var.get('v').callprop('match', var.get('w')))
                if ((var.get(u"null")==var.get('x')) or (Js(0.0)==var.get('x').get('length'))):
                    return Js([])
                #for JS loop
                var.put('y', Js(0.0))
                while (var.get('y')<var.get('x').get('length')):
                    try:
                        var.get('x').put(var.get('y'), (var.get('x').get(var.get('y'))+Js('')).callprop('trim'))
                    finally:
                            (var.put('y',Js(var.get('y').to_number())+Js(1))-Js(1))
                return var.get('x')
            PyJs_anonymous_39_._set_name('anonymous')
            var.get('k').put('exports', Js({'tokenizeInput':PyJs_anonymous_39_}))
        PyJs_anonymous_38_._set_name('anonymous')
        @Js
        def PyJs_anonymous_40_(this, arguments, var=var):
            var = Scope({'this':this, 'arguments':arguments}, var)
            var.registers(['j'])
            @Js
            def PyJsHoisted_j_(k, l, m, this, arguments, var=var):
                var = Scope({'k':k, 'l':l, 'm':m, 'this':this, 'arguments':arguments}, var)
                var.registers(['v', 'l', 'q', 's', 'm', 'k'])
                @Js
                def PyJsHoisted_q_(w, x, this, arguments, var=var):
                    var = Scope({'w':w, 'x':x, 'this':this, 'arguments':arguments}, var)
                    var.registers(['w', 'x', 'A', 'y', 'z'])
                    if var.get('l').get(var.get('w')).neg():
                        if var.get('k').get(var.get('w')).neg():
                            var.put('y', ((Js('function')==var.get('require',throw=False).typeof()) and var.get('require')))
                            if (var.get('x').neg() and var.get('y')):
                                return var.get('y')(var.get('w'), Js(0.0).neg())
                            if var.get('s'):
                                return var.get('s')(var.get('w'), Js(0.0).neg())
                            var.put('z', var.get('Error').create(((Js("Cannot find module '")+var.get('w'))+Js("'"))))
                            PyJsTempException = JsToPyException(PyJsComma(var.get('z').put('code', Js('MODULE_NOT_FOUND')),var.get('z')))
                            raise PyJsTempException
                        var.put('A', var.get('l').put(var.get('w'), Js({'exports':Js({})})))
                        @Js
                        def PyJs_anonymous_41_(B, this, arguments, var=var):
                            var = Scope({'B':B, 'this':this, 'arguments':arguments}, var)
                            var.registers(['C', 'B'])
                            var.put('C', var.get('k').get(var.get('w')).get('1').get(var.get('B')))
                            return var.get('q')((var.get('C') or var.get('B')))
                        PyJs_anonymous_41_._set_name('anonymous')
                        var.get('k').get(var.get('w')).get('0').callprop('call', var.get('A').get('exports'), PyJs_anonymous_41_, var.get('A'), var.get('A').get('exports'), var.get('j'), var.get('k'), var.get('l'), var.get('m'))
                    return var.get('l').get(var.get('w')).get('exports')
                PyJsHoisted_q_.func_name = 'q'
                var.put('q', PyJsHoisted_q_)
                pass
                #for JS loop
                var.put('s', ((Js('function')==var.get('require',throw=False).typeof()) and var.get('require')))
                var.put('v', Js(0.0))
                while (var.get('v')<var.get('m').get('length')):
                    try:
                        var.get('q')(var.get('m').get(var.get('v')))
                    finally:
                            (var.put('v',Js(var.get('v').to_number())+Js(1))-Js(1))
                return var.get('q')
            PyJsHoisted_j_.func_name = 'j'
            var.put('j', PyJsHoisted_j_)
            pass
            return var.get('j')
        PyJs_anonymous_40_._set_name('anonymous')
        return PyJs_anonymous_40_()(Js({'1':Js([PyJs_anonymous_1_, Js({})]),'2':Js([PyJs_anonymous_2_, Js({'./maps':Js(3.0),'./states/clocktime':Js(4.0),'./states/day':Js(5.0),'./states/frequency':Js(6.0),'./states/hour':Js(7.0),'./states/minute':Js(8.0),'./states/month':Js(9.0),'./states/range':Js(10.0),'./states/year':Js(11.0),'./tokens':Js(12.0),'readline':Js(1.0)})]),'3':Js([PyJs_anonymous_7_, Js({})]),'4':Js([PyJs_anonymous_9_, Js({'../maps':Js(3.0)})]),'5':Js([PyJs_anonymous_13_, Js({'../maps':Js(3.0)})]),'6':Js([PyJs_anonymous_17_, Js({'../maps':Js(3.0)})]),'7':Js([PyJs_anonymous_20_, Js({'../maps':Js(3.0)})]),'8':Js([PyJs_anonymous_23_, Js({'../maps':Js(3.0)})]),'9':Js([PyJs_anonymous_26_, Js({'../maps':Js(3.0)})]),'10':Js([PyJs_anonymous_31_, Js({'../maps':Js(3.0)})]),'11':Js([PyJs_anonymous_34_, Js({'../maps':Js(3.0)})]),'12':Js([PyJs_anonymous_38_, Js({'./maps':Js(3.0)})])}), Js({}), Js([Js(2.0)]))
    return PyJs_LONG_42_()(Js(2.0))
PyJs_anonymous_0_._set_name('anonymous')
@Js
def PyJs_anonymous_43_(b, this, arguments, var=var):
    var = Scope({'b':b, 'this':this, 'arguments':arguments}, var)
    var.registers(['b', 'd'])
    if ((Js('object')==var.get('exports',throw=False).typeof()) and (Js('undefined')!=var.get('module',throw=False).typeof())):
        var.get('module').put('exports', var.get('b')())
    else:
        if ((Js('function')==var.get('define',throw=False).typeof()) and var.get('define').get('amd')):
            var.get('define')(Js([]), var.get('b'))
        else:
            pass
            PyJsComma(var.put('d', (((var.get(u"this") if (Js('undefined')==var.get('self',throw=False).typeof()) else var.get('self')) if (Js('undefined')==var.get('global',throw=False).typeof()) else var.get('global')) if (Js('undefined')==var.get('window',throw=False).typeof()) else var.get('window'))),var.get('d').put('getCronString', var.get('b')()))
PyJs_anonymous_43_._set_name('anonymous')
PyJs_anonymous_43_(PyJs_anonymous_0_)
pass


# Add lib to the module scope
natural_cron = var.to_python()