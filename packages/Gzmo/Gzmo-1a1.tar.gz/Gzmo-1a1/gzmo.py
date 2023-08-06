# Standard library imports.
import argparse
import copy
import json
import re
import sys
from _io import TextIOWrapper
from datetime import datetime as _dt
from datetime import timedelta as _td
from zoneinfo import ZoneInfo as ZI


# Define a tuple of the allowable object types that can be queried for
# data.
TYPES = (
    type({}), type([]), type(''), type(0.1), type(0), type(True), type(None),)

# Define functions that wrap conditional statements.
CO_FUNCS = (
    ('cond', lambda x, y: True if x == True and y == True else False),
    ('coor', lambda x, y: True if x == True or y == True else False),)

# These are the lambda functions that test for equality.
EQ_FUNCS = (
    ('eqgt', lambda x, y: x > y),
    ('eqge', lambda x, y: x >= y),
    ('eqeq', lambda x, y: x == y),
    ('eqne', lambda x, y: x != y),
    ('eqle', lambda x, y: x <= y),
    ('eqlt', lambda x, y: x < y))

EQ_SYMBOLS = ('>', '>=', '==', '!=', '<=', '<',)


# The special mapping method will return an instance of this class.
class GMap:
    def __init__(self, key, obj, null = False):
        self.key, self.value, self.null = (str(key), obj, null,)


# The special select method will return an instance of this class.
class GSlc:
    def __init__(self, obj):
        self.value = obj


class P:

    def __init__(self):

        # Define the environment that will be used to evaluate the
        # input expressions.
        self.env = {'__builtins__': {}, 'o': None}

        # Populate the '__builtins__' with the instance methods in
        # this class.
        for attr in dir(self):

            if attr.startswith('_P__f_'):

                obj = getattr(self, attr, None)

                if callable(obj):
                    self.env['__builtins__'][attr[6:]] = obj

        for co in CO_FUNCS:
            self.env['__builtins__'][co[0]] = co[1]

        for eq in EQ_FUNCS:
            self.env['__builtins__'][eq[0]] = eq[1]

        # Add the special methods.  These are methods that access
        # and/or change the eval environment.
        self.env['__builtins__'].update(
            {
                'gmap': self.__s_gmap,
                'gslc': self.__s_gslc,
                'svar': self.__s_svar})

        # The following instance variable is set when the program is
        # evaluating code after a generator is created.
        self.gen_loop = False

        return None

    def __f_dprs(self, obj, tmpl, tz = None, to_tz = None):

        try:

            d = _dt.strptime(obj, tmpl)

            if (tz != None) and (to_tz != None):
                d = _dt.combine(d.date(), d.time(), ZI(tz))\
                    .astimezone(ZI(to_tz))

        except:
            d = None

        if d != None:
            d = str(d)

        return d

    def __f_fltr(self, obj, index, symb, value):

        if symb in EQ_SYMBOLS:

            if type(index) == type(None):

                f = {'symb': symb, 'value': value}
                exec('_ = lambda x: x {symb} {value}'.format(f))

            elif type(index) in (type(''), type(0),):

                f = {'index': str(index), 'symb': symb, 'value': value}
                exec('_ = lambda x: x[{index}] {symb} {value}'.format(**f))

            else:
                exec('_ = lambda x: True')

            ffunc = locals()['_']

            if 'generator' in str(type(obj)):
                fltrd = filter(ffunc, obj)

            elif type(obj) == type([]):
                fltrd = filter(ffunc, (x for x in obj))

            else:
                raise Exception('obj is not an iterable or a generator')

        else:
            raise Exception('Invalid equality symbol')

        return list(fltrd)

    def __f_genr(self, obj):

        if type(obj) == type([]):
            obj = (x for x in obj)

        else:
            raise Exception('Cannot create generator from obj')

        return obj

    def __f_getv(self, obj, index):

        if type(obj) == type({}):
            value = obj.get(index, None)

        elif type(obj) == type([]):

            try:
                value = obj[index]

            except:
                value = None

        else:
            value = None

        return value

    def __f_keys(self, obj):

        if type(obj) == type([]):
            keys = list(range(len(obj)))

        elif type(obj) == type({}):
            keys = obj.keys()

        else:
            keys = None

        return keys

    def __f_olen(self, obj):

        return len(obj)

    def __f_stat(self, obj):

        # Use this variable to store statistics.  If the input object
        # is a list of numbers, then the stats will be a dictionary.
        # Otherwise, if the input object is a list of lists, then
        # the stats will be a list containing stats dictionaries for
        # each element of the first list in the input object.  If the
        # input object is a list of dictionaries, the stats will be
        # a dictionary of stats dictionaries for each key in the first
        # dictionary in input object.
        stats = None

        # Set the type of the first element in the input object list
        # using this variable.
        ftype = None

        # Call to create an empty stats dictionary.
        def _e():
            return {'max': None, 'min': None, 'avg': None, 'num': 0, 'sum': 0}

        # Use this function internally to help calculate the list's
        # statistics.
        def _s(i, v, s):

            if type(v) in (type(0), type(0.0),):

                if s['max'] == None:
                    s['max'] = {'obj': i, 'val': v}

                elif v > s['max']['val']:
                    s['max'] = {'obj': i, 'val': v}

                if s['min'] == None:
                    s['min'] = {'obj': i, 'val': v}

                elif v < s['min']['val']:
                    s['min'] = {'obj': i, 'val': v}

                s['num'] += 1
                s['sum'] += v
                s['avg'] = s['sum'] / s['num']

            return s

        if type(obj) == type([]):

            counter = 0

            for i in obj:

                if ftype == None:
                    ftype = type(i)

                if stats == None:

                    if ftype == type({}):

                        stats = {}

                        for j in i.keys():
                            stats[j] = _e()

                    elif ftype == type([]):

                        stats = [None] * len(i)

                        for j in range(0, len(i)):
                            stats[j] = _e()

                    elif ftype in (type(0), type(0.0)):
                        stats = _e()

                if type(i) != ftype:
                    raise Exception('Mismatched types calculating stats')

                elif type(i) == type({}):
                    for j in i.keys():
                        if j in stats.keys():
                            _s(i, i[j], stats[j])

                elif type(i) == type([]):
                    if len(i) == len(stats):
                        for j in range(0, len(i)):
                            _s(i, i[j], stats[j])

                else:
                    _s(counter, i, stats)

                counter += 1

        if stats != None:

            if ftype == type({}):
                for j in stats.keys():
                    if stats[j]['num'] == 0:
                        stats[j] = None

            if ftype == type([]):
                for j in range(0, len(stats)):
                    if stats[j]['num'] == 0:
                        stats[j] = None

        return stats

    def __f_trim(self, obj, start, end):

        try:
            value = obj[start:end]

        except:
            value = None

        return value

    def __s_gmap(self, key, obj):

        mapped = GMap(key, obj)

        if self.gen_loop == True:

            if type(obj) == type(GSlc(None)):

                if obj.value != None:
                    mapped = GMap(key, obj.value)

                else:
                    mapped = GMap(None, None, null = True)

        else:

            msg = 'gmap can only be used in the stage after a generator '\
                + 'is created'
            raise Exception(msg)

        return mapped

    def __s_gslc(self, is_selected, obj):

        selected = GSlc(obj)

        if self.gen_loop == True:

            if is_selected == True:

                if type(obj) == type(GMap(None, None)):
                    selected = obj

            else:

                if type(obj) == type(GMap(None, None)):
                    selected = GMap(None, None, null = True)

                else:
                    selected = GSlc(None)

        else:

            msg = 'gslc can only be used in the stage after a generator '\
                + 'is created'
            raise Exception(msg)

        return selected

    def __s_svar(self, name, value):

        reserved = ['__builtins__', 'o']\
            + list(self.env['__builtins__'].keys())
        match = re.match('^[^\d][A-Za-z0-9_]*$', name)

        if (name not in reserved) and (match != None):
            self.env[name] = value

        else:
            raise Exception(name + ' is not a valid variable name')

        return self.env['o']

    def _parse_exprs(self, pstr):

        # Create a temporary string of expressions with underscores
        # replacing any quoted substrings (they may have spaces or
        # the pipe symbol).
        tmp = list(pstr)

        for r in re.finditer('"([^"]*)"', pstr):

            span = r.span()

            for i in range(span[0] + 1, span[1] - 1):
                tmp[i] = '_'

        tmp = "".join(tmp)

        # Slice up the process string by the pipe symbol into Python
        # expressions.
        exprs = []
        pos = 0

        for r in re.finditer('\|', tmp):

            exprs.append(pstr[pos:r.span()[0]].strip())
            pos = r.span()[1]

        if pos < len(pstr):
            exprs.append(pstr[pos:].strip())

        return exprs

    def _p(self, obj, pstr, **extras):

        if type(obj) in TYPES:
            self.env['o'] = copy.deepcopy(obj)

        # If any extra functions or variables are given in the extras
        # arguments, add them to the evaluation namespace.
        for k in extras.keys():
            if (callable(extras[k])) or type(extras[k]) in TYPES:
                self.__f_svar(k, extras[k])

        # Parse the expressions from the process string, then evaluate
        # each expression in the following loop.  Remember that in most
        # cases, the result of the evaluation is made available for the
        # next expression to be evaluated.
        for expr in self._parse_exprs(pstr):

            try:

                if 'generator' in str(type(self.env['o'])):

                    # Make sure that the slct method (if specified in
                    # the expression) knows that we are in the
                    # generator loop.
                    self.gen_loop = True

                    # Data from the generator loop will be stored using
                    # this variable.  If the data is a "primative,"
                    # then this variable will be a list.  If the data
                    # is a result of the mapping method, then the
                    # variable will initially be a dictionary.  If the
                    # data is a result of a the select method, then
                    # the result will be a list.
                    gres = None

                    # Execute the generator.  As the generator is
                    # iterated, the "o" value will be updated with
                    # the current value of the iterator.
                    for i in self.env['o']:

                        self.env['o'] = i
                        _ =  eval(expr, self.env, {})

                        if type(_) == type(()):
                            _ = list(_)

                        if type(_) == type(GMap(None, None)):

                            if gres == None:
                                gres = {}

                            if _.null != True:

                                if _.key not in gres.keys():
                                    gres[_.key] = []

                                gres[_.key].append(_.value)

                        elif type(_) == type(GSlc(None)):

                            if gres == None:
                                gres = []

                            if _.value != None:
                                gres.append(_.value)

                        else:

                            if gres == None:
                                gres = []

                            gres.append(_)

                    # Set the results of the iteration back into the
                    # eval environment.
                    self.env['o'] = gres

                else:
                    self.env['o'] = eval(expr, self.env, {})

            except NameError as e:
                raise Exception(str(e)) from None

            except SyntaxError as e:

                msg = '\'' + e.text[e.offset -1:e.end_offset - 1] + '\''
                raise Exception(msg + ' from ' + '\'' + expr + '\'') from None

            except TypeError as e:
                raise Exception(str(e)) from None

            except Exception as e:
                raise Exception(str(e)) from None

            # Before the next evaluation occurs, make sure that the
            # gen_loop flag is set to false.
            self.gen_loop = False

        # If the data object is a generator after all the process
        # strings have been evaluated, then generate a list as the
        # final data structure to be returned.
        if 'generator' in str(type(self.env['o'])):
            self.env['o'] = list(self.env['o'])

        return self.env['o']


def p(obj, pstr, **extras):

    # Create the process instance and return the results of the
    # evaluations of the process strings.
    return P()._p(obj, pstr, **extras)


def main():

    # Set the result of the processing to this variable for output via
    # stdout.
    output = ''

    parser = argparse.ArgumentParser()
    parser.add_argument(
        'qstr',
        type = str,
        help = 'A string of expressions used to process the given JSON data')
    parser.add_argument(
        '-i',
        '--input-file',
        type = argparse.FileType('r'),
        default = (None if sys.stdin.isatty() else sys.stdin))
    parser.add_argument(
        '-o',
        '--output-file',
        type = argparse.FileType('w'),
        default = sys.stdout)

    args = parser.parse_args()

    if type(args.input_file) == TextIOWrapper:

        try:
            contents = args.input_file.read()

        except:
            contents = None

        if contents != None:

            try:
                data = json.loads(contents)

            except:
                data = {}

            output = json.dumps(p(data, args.qstr), indent = 1)

    # Output the processed data to stdout.
    if type(output) == type(''):
        args.output_file.write(output + '\n')

    # Explicitly exit the script.
    sys.exit(0)


if __name__ == '__main__':
    main()
