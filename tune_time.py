import re
import datetime
import getopt
import sys


def trans_time_forward(ldata, delta):
    [st, et] = ldata.split('-->')
    st = st.strip()
    et = et.strip()
    stt = datetime.datetime.strptime(st, '%H:%M:%S,%f')
    ett = datetime.datetime.strptime(et, '%H:%M:%S,%f')
    td = datetime.timedelta(milliseconds=delta)
    nstt = stt + td
    nett = ett + td
    snstt = '{0}'.format(nstt.strftime('%H:%M:%S,%f'))
    snett = '{0}'.format(nett.strftime('%H:%M:%S,%f'))

    return '{0} --> {1}\n'.format(snstt[:-3], snett[:-3])


def do_transform():
    input_error = 0
    in_file = None
    in_encoding = None
    out_file = None
    out_encoding = None
    out_time = 0
    start_index = 0
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'i:o:e:t:', [])
        if len(opts) == 0:
            input_error = 1
        else:
            for opt, arg in opts:
                if opt == '-i':
                    in_file = arg
                elif opt == '-o':
                    out_file = arg
                elif opt == '-e':
                    in_encoding = arg
                elif opt == '-t':
                    out_time = int(arg)
                elif opt == '-d':
                    out_encoding = arg
                elif opt == '-b':
                    start_index = int(arg)
    except Exception as e:
        input_error = 1
        print(e)
    finally:
        if input_error == 1 or out_time == 0 or in_file == out_file:
            help_msg = '''usage:
            -i                   : input file name
            -o                   : output file name
            -b                   : section start to trans
            -e                   : encoding of input file (gbk,utf8 etc.)
            -d                   : encoding of output file (gbk,utf8 etc.)
            -t                   : forward time ([-1]milliseconds)
            -h                   : help message'''
            print (help_msg)
            sys.exit(0)

    if in_encoding is None:
        in_encoding = 'utf8'
    if out_encoding is None:
        out_encoding = 'utf8'

    index = 0
    with open(in_file, mode='r', encoding=in_encoding) as f:
        with open(out_file, mode='w', encoding=out_encoding) as fout:
            while True:
                ldata = f.readline()
                if not ldata:
                    break
                if re.match('[0-9]{2}:[0-9]{2}:[0-9]{2},[0-9]{3} -->', ldata):
                    if index >= start_index:
                        index += 1
                        fout.write(trans_time_forward(ldata, out_time))
                    else:
                        fout.write(ldata)
                else:
                    fout.write(ldata)


do_transform()
