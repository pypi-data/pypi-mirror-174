import pandas as pd
import numpy as np



def zigzag(df, timecorrection=3, pricecorrection=0.33, four_one_rule=1, zigtrendcheck=1,
                               zighorizanteltrendl=1, **kwargs):
    """Indicator: ZIGZAG"""

    # open=df['open']
    # high=df['high']
    # low = df['low']
    # close = df['close']


    # Validate Arguments
    # length = length if length and length > 0 else 14
    # lensig = lensig if lensig and lensig > 0 else length
    # mamode = mamode if isinstance(mamode, str) else "rma"
    # scalar = float(scalar) if scalar else 100
    #
    # high = verify_series(high, length)
    # low = verify_series(low, length)
    # close = verify_series(close, length)
    # open = verify_series(open, length)
    # drift = get_drift(drift)
    # offset = get_offset(offset)

    
    count = 1
    zigvariable = {}

    if four_one_rule==1:
        up_loopind=-1
        dn_loopind=1
    else:
        up_loopind = -10
        dn_loopind = 10

    for index1, row in df.iterrows():
        sub_df = df.iloc[:count]
        # print(sub_df)
        # print('row',row)
        # print('index1',index1)
        zigvariable = zig_line_feed_data(row, index1, count, zigvariable, sub_df, timecorrection, pricecorrection, up_loopind,
                                         dn_loopind)
        
        # if count>195:
        #     print(zigvariable)
        #     break

        count = count + 1
    
    zig_df = HL_LL_LH_HH(sub_df, zigvariable['zigzag_xdata'], zigvariable['zigzag_ydata'],
                         zigvariable['index_list_count'],
                         zigvariable['zigline'])



    if zigtrendcheck==1:
        trend_list = tend_segment(zig_df)
    else:
        trend_list=None

    if zighorizanteltrendl==1:
        allvalid_zig_HZ_trendlines = cal_hzig_lines(zig_df)
    else:
        allvalid_zig_HZ_trendlines=None

    valid_breakup_price, valid_breakdn_price=cal_breakup(zig_df, allvalid_zig_HZ_trendlines)



    return zig_df,trend_list,allvalid_zig_HZ_trendlines,valid_breakup_price, valid_breakdn_price
def zig_line_feed_data(row, index, count, zigvariable, df,time_correc, price_correc,up_loopind,dn_loopind):
    curcan = [row['open'], row['high'], row['close'], row['low']]
    currhigh = max(curcan)
    currlow = min(curcan)

    if count > 1:
        zigvariable['currlow'] = currlow
        zigvariable['currhigh'] = currhigh

        #         # print(zigvariable)
        rangedata = zigvariable['rangedata']
        rangedataup = zigvariable['rangedataup']
        rangedatadn = zigvariable['rangedatadn']
        upmov = zigvariable['upmov']
        dnmov = zigvariable['dnmov']
        upcont = zigvariable['upcont']
        dncont = zigvariable['dncont']

        secupcont = zigvariable['secupcont']
        secdncont = zigvariable['secdncont']
        gppoint = zigvariable['gppoint']
        zigline = zigvariable['zigline']
        zigzag_ydata = zigvariable['zigzag_ydata']
        zigzag_xdata = zigvariable['zigzag_xdata']
        canlen = zigvariable['canlen']
        index_list_count = zigvariable['index_list_count']

        index_list_count.update({index: count})

        contrnd = None
        if len(zigzag_ydata) > 1:
            if currhigh > rangedataup[0] and currlow < rangedatadn[1]:
                # lastrndcheck = list(gppoint[-1].values())[0][0]
                # check_ind = checknextmove(df, count, lastrndcheck, zigline[-1])


                contrnd = check_next_move(gppoint, df, count, zigline)


    if count == 1:
        zigvariable = first_zig_move(count, index, currhigh, currlow,time_correc, price_correc)


    elif currhigh > rangedataup[0] and currlow > rangedataup[1] or contrnd == 'up':
        # print('upsearch for cont',count)

        try:
            seconlastcheck = canlen[-2][2]
        except:
            seconlastcheck = currhigh + 1

        upcont = upcont + 1



        if canlen[-1][0] == up_loopind and currhigh > seconlastcheck and canlen[-1][
            1] + upcont < 6 and len(gppoint) > 3:

            # print('upsearch: No noraml')
            zigvariable=rule4_1_upmove(count, index, zigvariable,df)



        else:
            # print('upsearch: noraml')
            rangedataup = [currhigh, rangedataup[1]]
            secupcont = secupcont + 1

            zigvariable['rangedataup'] = rangedataup
            zigvariable['secupcont'] = secupcont
            zigvariable['seconlastcheck'] = seconlastcheck
            zigvariable['upcont'] = upcont

            if currhigh > upmov:
                zigvariable = upmove_normal(count, index, zigvariable)


    elif currhigh < rangedatadn[0] and currlow < rangedatadn[1] or \
            contrnd == 'dn':  # for
        # downside trend
        # # print('Downtrend Search for count', count)
        # print('dnsearchfor cont',count)

        try:
            seconlastcheck = canlen[-2][2]
        except:
            seconlastcheck = currlow - 1

        dncont = dncont + 1

        if canlen[-1][0] == dn_loopind and currlow < seconlastcheck and canlen[-1][
            1] + dncont < 6 and len(gppoint) > 3:
            # print('dnsearch:no normal')

            zigvariable=rule4_1_dnmove(count, index, zigvariable,df)

        else:
            # print('dnsearch:normal')

            rangedatadn = [rangedatadn[0], currlow]
            secdncont = secdncont + 1

            zigvariable['rangedatadn'] = rangedatadn
            zigvariable['secdncont'] = secdncont
            zigvariable['seconlastcheck'] = seconlastcheck
            zigvariable['dncont'] = dncont

            if currlow < dnmov:
                zigvariable = dnmovenormal(count, index, zigvariable)
    else:
        aa = 1
        # print('no move')

    zigline = zigvariable['zigline']
    if len(zigline) > 2 and count > 1:
        Fdata = zigline[-2]
        Edata = zigline[-1]
        stdate = zigzag_xdata[-2]
        endate = zigzag_xdata[-1]
        # print(stdate)

        candel_value = getcandnum(df, Fdata, Edata, stdate, endate)
        #         # print('candel_value', candel_value)
        canlen[-1][1] = candel_value
        temp_array_canlen = canlen.copy()

    return zigvariable
def checknextmove1(df, count, lastrndcheck, last_point):
    IND = -1
    upcn = 0
    dncn = 0
    val = 0

    point_iloc = count - 1

    #     # print(last_point)
    last_lo_poi = list(last_point.keys())[0]
    #     # print(last_lo_poi)
    #     # print(count)

    if count - last_lo_poi > 1:

        while IND < 100:
            curentdf = df.iloc[last_lo_poi + IND]
            nextdf = df.iloc[last_lo_poi + IND + 1]
            #             # print(curentdf,nextdf)
            if curentdf['low'] > nextdf['low']:
                dncn = dncn + 1
            if curentdf['high'] < nextdf['high']:
                upcn = upcn + 1

            #             # print('ATT=',IND,dncn,upcn)
            if last_lo_poi + IND == point_iloc - 1:
                break

            IND = IND + 1

        if dncn > upcn and lastrndcheck == 1:
            val = -1
        elif upcn > dncn and lastrndcheck == -1:
            val = 1
        elif upcn == dncn:
            if lastrndcheck == 1:
                val = 1
            else:
                val = -1
        else:
            pass
    else:

        if lastrndcheck == 1:
            val = 1
        else:
            val = -1

    return val
def check_next_move(gppoint, df, count, zigline):
    lastrndcheck = list(gppoint[-1].values())[0][0]
    check_ind = checknextmove1(df, count, lastrndcheck, zigline[-1])
    if check_ind == 1:
        contrnd = 'up'
    else:
        contrnd = 'dn'

    return contrnd
def first_zig_move(count, index, currhigh, currlow,time_correc, price_correc):
    index_list_count = {}
    zigzag_ydata = []
    zigzag_xdata = []
    glbarcount = int(time_correc)
    maxbarcontdn = glbarcount
    maxbarcontup = glbarcount
    permv = float(price_correc)

    index_list_count.update({index: count})

    rangedata = [currhigh, currlow]
    rangedataup = [currhigh, currlow]
    rangedatadn = [currhigh, currlow]

    upmov = currlow
    dnmov = currhigh

    upcont = 1
    dncont = 1

    secupcont = 1
    secdncont = 1

    gppoint = [{count: [0, currlow]}]
    zigline = [{count: [0, currlow]}]
    zigzag_ydata.append(currlow)
    zigzag_xdata.append(index)
    canlen = [[0, 0, 0], [-1, 0, currlow]]

    zigvariable = {'rangedata': rangedata,
                   'rangedataup': rangedataup,
                   'rangedatadn': rangedatadn,
                   'upmov': upmov,
                   'dnmov': dnmov,
                   'upcont': upcont,
                   'dncont': dncont,
                   'secupcont': secupcont,
                   'secdncont': secdncont,
                   'gppoint': gppoint,
                   'zigline': zigline,
                   'zigzag_ydata': zigzag_ydata,
                   'zigzag_xdata': zigzag_xdata,
                   'canlen': canlen,
                   'index_list_count': index_list_count,
                   'currlow': currlow,
                   'currhigh': currhigh,
                   'glbarcount': glbarcount,
                   'maxbarcontdn': maxbarcontdn,
                   'maxbarcontup': maxbarcontup,
                   'permv': permv
                   }

    return zigvariable
def upmove_normal(count, index, zigvariable):
    #     # print('in up')
    #     # print(zigvariable)

    rangedata = zigvariable['rangedata']
    rangedataup = zigvariable['rangedataup']
    rangedatadn = zigvariable['rangedatadn']
    upmov = zigvariable['upmov']
    dnmov = zigvariable['dnmov']
    upcont = zigvariable['upcont']
    dncont = zigvariable['dncont']

    secupcont = zigvariable['secupcont']
    secdncont = zigvariable['secdncont']
    gppoint = zigvariable['gppoint']
    zigline = zigvariable['zigline']
    zigzag_ydata = zigvariable['zigzag_ydata']
    zigzag_xdata = zigvariable['zigzag_xdata']
    canlen = zigvariable['canlen']
    index_list_count = zigvariable['index_list_count']

    currhigh = zigvariable['currhigh']
    currlow = zigvariable['currlow']
    seconlastcheck = zigvariable['seconlastcheck']
    maxbarcontdn = zigvariable['maxbarcontdn']
    maxbarcontup = zigvariable['maxbarcontup']
    permv = zigvariable['permv']
    glbarcount = zigvariable['glbarcount']

    # print(zigvariable['zigline'])
    # print(zigvariable['gppoint'])
    # print(zigvariable['canlen'])

    exp_rule_4_1_up = 0
    if len(gppoint) > 3 and canlen[-1][
        0] == -1 and currhigh > seconlastcheck and canlen[-1][
        1] > 3 and upcont == 2 and maxbarcontup > upcont:
        exp_rule_4_1_up = 1

    if upcont >= maxbarcontup or exp_rule_4_1_up == 1:
        # print('Final UP TREND POINT FOUND for count', count)
        maxbarcontup = 1
        maxbarcontdn = glbarcount

        upcont = 1
        dncont = 1

        rangedataup = [currhigh, currlow]
        rangedatadn = [currhigh, currlow]

        zigvariable['maxbarcontup'] = maxbarcontup
        zigvariable['maxbarcontdn'] = maxbarcontdn
        zigvariable['upcont'] = upcont
        zigvariable['dncont'] = dncont
        zigvariable['rangedataup'] = rangedataup
        zigvariable['rangedatadn'] = rangedatadn

        uppoint = {count: [1, currhigh]}
        gppoint.append(uppoint)

        if list(gppoint[-2].values())[0][0] == 1:
            #             #                             #                             # print(gppoint)
            #             #                             #                             # print(zigline)
            #             #                             #                             # print(uppoint)
            zigline[-1] = uppoint
            zigzag_ydata[-1] = currhigh
            zigzag_xdata[-1] = index

            canlen[-1] = [1, secupcont, currhigh]

        else:
            zigline.append(uppoint)
            zigzag_ydata.append(currhigh)
            zigzag_xdata.append(index)

            # lenc = list(zigline[-1].keys())[0] - list(zigline[-2].keys())[0]
            canlen.append([1, secupcont, currhigh])

        TOTALMOVE = list(zigline[-1].values())[0][1] - \
                    list(zigline[-2].values())[0][1]
        dnmov = list(zigline[-1].values())[0][
                    1] - TOTALMOVE * permv

        zigvariable['gppoint'] = gppoint
        zigvariable['zigline'] = zigline
        zigvariable['zigzag_ydata'] = zigzag_ydata
        zigvariable['zigzag_xdata'] = zigzag_xdata
        zigvariable['canlen'] = canlen
        zigvariable['dnmov'] = dnmov

    # print(zigvariable['zigline'])
    # print(zigvariable['gppoint'])
    # print(zigvariable['canlen'])
    # print('end loop')
    return zigvariable
def dnmovenormal(count, index, zigvariable):
    rangedata = zigvariable['rangedata']
    rangedataup = zigvariable['rangedataup']
    rangedatadn = zigvariable['rangedatadn']
    upmov = zigvariable['upmov']
    dnmov = zigvariable['dnmov']
    upcont = zigvariable['upcont']
    dncont = zigvariable['dncont']

    secupcont = zigvariable['secupcont']
    secdncont = zigvariable['secdncont']
    gppoint = zigvariable['gppoint']
    zigline = zigvariable['zigline']
    zigzag_ydata = zigvariable['zigzag_ydata']
    zigzag_xdata = zigvariable['zigzag_xdata']
    canlen = zigvariable['canlen']
    index_list_count = zigvariable['index_list_count']

    currhigh = zigvariable['currhigh']
    currlow = zigvariable['currlow']
    seconlastcheck = zigvariable['seconlastcheck']
    maxbarcontdn = zigvariable['maxbarcontdn']
    maxbarcontup = zigvariable['maxbarcontup']
    permv = zigvariable['permv']
    glbarcount = zigvariable['glbarcount']

    # print(zigvariable['zigline'])
    # print(zigvariable['gppoint'])
    # print(zigvariable['canlen'])

    exp_rule_4_2 = 0
    if len(gppoint) > 3 and canlen[-1][
        0] == 1 and currlow < seconlastcheck and canlen[-1][
        1] > 3 and dncont == 2 and maxbarcontdn > dncont:
        #         # print('four + 2 rule here')
        exp_rule_4_2 = 1

    if dncont >= maxbarcontdn or exp_rule_4_2 == 1:
        # print('Final DN TREND POINT FOUND for count', count)
        maxbarcontup = glbarcount
        maxbarcontdn = 1

        upcont = 1
        dncont = 1

        rangedataup = [currhigh, currlow]
        rangedatadn = [currhigh, currlow]

        zigvariable['maxbarcontup'] = maxbarcontup
        zigvariable['maxbarcontdn'] = maxbarcontdn
        zigvariable['upcont'] = upcont
        zigvariable['dncont'] = dncont
        zigvariable['rangedataup'] = rangedataup
        zigvariable['rangedatadn'] = rangedatadn

        dnpoint = {count: [-1, currlow]}
        gppoint.append(dnpoint)

        if list(gppoint[-2].values())[0][0] == -1:
            zigline[-1] = dnpoint
            zigzag_ydata[-1] = currlow
            zigzag_xdata[-1] = index

            # canlen[-1] = list(zigline[-1].keys())[0] - list(zigline[-2].keys())[0]
            canlen[-1] = [-1, secdncont, currlow]

        else:
            zigline.append(dnpoint)
            zigzag_ydata.append(currlow)
            zigzag_xdata.append(index)

            # lenc = list(zigline[-1].keys())[0] - list(zigline[-2].keys())[0]
            canlen.append([-1, secdncont, currlow])

        TOTALMOVE = list(zigline[-2].values())[0][1] - \
                    list(zigline[-1].values())[0][1]
        upmov = list(zigline[-1].values())[0][
                    1] + TOTALMOVE * permv

        zigvariable['gppoint'] = gppoint
        zigvariable['zigline'] = zigline
        zigvariable['zigzag_ydata'] = zigzag_ydata
        zigvariable['zigzag_xdata'] = zigzag_xdata
        zigvariable['canlen'] = canlen
        zigvariable['upmov'] = upmov

    # print(zigvariable['zigline'])
    # print(zigvariable['gppoint'])
    # print(zigvariable['canlen'])
    # print('end loop')

    return zigvariable
def rule4_1_upmove(count, index, zigvariable, df):
    # print('now in up suitation at =', count)
    rangedata = zigvariable['rangedata']
    rangedataup = zigvariable['rangedataup']
    rangedatadn = zigvariable['rangedatadn']
    upmov = zigvariable['upmov']
    dnmov = zigvariable['dnmov']
    upcont = zigvariable['upcont']
    dncont = zigvariable['dncont']

    secupcont = zigvariable['secupcont']
    secdncont = zigvariable['secdncont']
    gppoint = zigvariable['gppoint']
    zigline = zigvariable['zigline']
    zigzag_ydata = zigvariable['zigzag_ydata']
    zigzag_xdata = zigvariable['zigzag_xdata']
    canlen = zigvariable['canlen']
    index_list_count = zigvariable['index_list_count']

    currhigh = zigvariable['currhigh']
    currlow = zigvariable['currlow']
    seconlastcheck = zigvariable['seconlastcheck']
    maxbarcontdn = zigvariable['maxbarcontdn']
    maxbarcontup = zigvariable['maxbarcontup']
    permv = zigvariable['permv']
    glbarcount = zigvariable['glbarcount']

    # print('currhigh==', currhigh)
    # print('zigzagvalue', canlen)
    maxcheck = min(5, len(zigline) - 1)
    foundid = 0

    # print(zigzag_xdata)
    for CII, check_candel in enumerate(reversed(zigline)):
        cand_num = list(check_candel.keys())[0]
        cand_value = list(check_candel.values())[0]
        # low_date = zigzag_xdata[-CII - 1]
        # print(cand_num, cand_value)
        if cand_value[1] > currhigh and cand_value[0] == 1:
            foundid = 1
            # print('found at', CII)
            # print('zigline00==', zigline)
            break

        if CII > maxcheck:
            break

    if foundid == 0:
        # if len(zigline) <= maxcheck:
        #     maxcheck = len(zigline) - 1
        #
        # print(maxcheck)
        # print(zigline)

        check_H_L = list(list(reversed(zigline))[maxcheck].values())[0][0]
        if check_H_L == -1:
            maxcheck = maxcheck - 1

        # st_p=list(reversed(zigline))[maxcheck]
        # end_p=zigline[-1]

        st_date = list(reversed(zigzag_xdata))[maxcheck]
        end_date = index

        Sdate_indexN = df.index.get_loc(st_date)
        Edate_indexN = df.index.get_loc(end_date)

        #
        # # print(st_p,end_p)
        # print(st_date, end_date)
        # print(Sdate_indexN,Edate_indexN)

        subdf = df.loc[st_date:end_date, :]

        #                     # print(subdf)

        low_value = subdf.loc[:, 'low'].min()
        low_valuedate = subdf.loc[:, 'low'].idxmin()

        count_low = index_list_count[low_valuedate]
        # print('AA=',low_value, low_valuedate,count_low)

        # print(zigline)

        for C1, lasthigh in enumerate(reversed(zigline)):
            can1_num = list(lasthigh.keys())[0]
            cand1_value = list(lasthigh.values())[0]
            # print(can1_num,cand1_value)
            if can1_num < count_low and cand1_value[0] == 1:
                CII = C1
                st_date = list(reversed(zigzag_xdata))[C1]
                break

        #                     # print(can1_num,cand1_value,st_date)

        subdf2 = subdf.loc[st_date:low_valuedate, :]
        # # print(subdf2)
        # print(low_valuedate)

        # CH_LOW = subdf2.iloc[0, 3]
        CH_LOW = subdf2.iloc[0, subdf2.columns.get_loc("low")]

        # print(CH_LOW)
        # subdf2.loc[subdf2['low'] < CH_LOW, 'CHECK LOW'] = 1
        # subdf2.loc[subdf2['low'] >= CH_LOW, 'CHECK LOW'] = 0
        subdf2.loc[subdf2.loc[:, 'low'] < CH_LOW, 'CHECK LOW'] = 1
        subdf2.loc[subdf2.loc[:, 'low'] >= CH_LOW, 'CHECK LOW'] = 0

        Total_low_cand = int(subdf2.loc[:, 'CHECK LOW'].sum()) + 1
        #                     # print(Total_low_cand)

        CNT1 = Total_low_cand
        xdata = low_valuedate

        CII = C1
        count_low = index_list_count[low_valuedate]
        # print(CII)



    else:
        # llc = df.index.get_loc(low_date)

        # st_p = list(reversed(zigline))[CII]
        # end_p = zigline[-1]

        st_date = list(reversed(zigzag_xdata))[CII]
        end_date = index

        Sdate_indexN = df.index.get_loc(st_date)
        Edate_indexN = df.index.get_loc(end_date)

        #
        # # print(st_p,end_p)
        # print(st_date, end_date)
        # print(Sdate_indexN,Edate_indexN)

        subdf3 = df.loc[st_date:end_date, :]
        # print(subdf3)
        # print('****')

        #                     # print(subdf3['low'])

        low_value = subdf3.loc[:, 'low'].min()
        low_valuedate = subdf3.loc[:, 'low'].idxmin()
        # print(low_value, low_valuedate)

        subdf4 = subdf3.loc[st_date:low_valuedate, :]
        # # print(subdf2)
        # print(low_valuedate)

        # CH_LOW = subdf4.iloc[0, 3]
        CH_LOW = subdf4.iloc[0, subdf4.columns.get_loc("low")]
        
        #                     # print(CH_LOW)
        subdf4.loc[subdf4.loc[:, 'low'] < CH_LOW, 'CHECK LOW'] = 1
        subdf4.loc[subdf4.loc[:, 'low'] >= CH_LOW, 'CHECK LOW'] = 0

        # print(subdf4)

        Total_low_cand = int(subdf4.loc[:, 'CHECK LOW'].sum()) + 1
        #                     # print(Total_low_cand)

        CNT1 = Total_low_cand
        xdata = low_valuedate
        count_low = index_list_count[low_valuedate]

        CII = CII

        # print(CNT1,xdata,CII)
        # print(low_value)


    if len(gppoint) > 2:
            # gppoint.pop()
            # zigline.pop()
            #
            # zigzag_ydata.pop()
            # zigzag_xdata.pop()
            # canlen.pop()
            # print(type(len(zigline)))
            # print('gp0=', gppoint)
            # print('zp0=', zigline)
            # print('cl0=', canlen)
            # print('xdata0=', zigzag_xdata)
            # print('ydata0=', zigzag_ydata)

        gppoint = gppoint[: len(gppoint) - CII]
        zigline = zigline[: len(zigline) - CII]
        canlen = canlen[: len(canlen) - CII]
        zigzag_ydata = zigzag_ydata[: len(zigzag_ydata) - CII]
        zigzag_xdata = zigzag_xdata[: len(zigzag_xdata) - CII]

            # print(type(len(zigline)))
            # print('gp1=', gppoint)
            # print('zp1=', zigline)
            # print('cl1=', canlen)
            # print('xdata1=', zigzag_xdata)
            # print('ydata1=', zigzag_ydata)

        # min_low=aa=df.iloc[l_index,3]
        # l_point = {count: [-1, list(low_value.values)[0]]}
    l_point = {count_low: [-1, low_value]}

    gppoint.append(l_point)
    zigline.append(l_point)
    zigzag_ydata.append(low_value)
    zigzag_xdata.append(xdata)
    canlen.append(([-1, CNT1, low_value]))

        # print(type(len(zigline)))
        # print('gp=', gppoint)
        # print('zp=', zigline)
        # print('cl=', canlen)
        # print('xdata=', zigzag_xdata)
        # print('ydata=', zigzag_ydata)

        # uiolio

    uppoint = {count: [1, currhigh]}
    secupcont = secupcont + 1
    zigvariable['secupcont'] = secupcont

    gppoint.append(uppoint)
    zigline.append(uppoint)
    zigzag_ydata.append(currhigh)
    zigzag_xdata.append(index)

        # canlen[-1] = list(zigline[-1].keys())[0] - list(zigline[-2].keys())[0]
    canlen.append(([1, secupcont, currhigh]))

        # print(type(len(zigline)))
        # print('gp==', gppoint)
        # print('zp==', zigline)
        # print('cl==', canlen)
        # print('xdata==', zigzag_xdata)
        # print('ydata==', zigzag_ydata)

    Fdata = zigline[-3]
    Edata = zigline[-2]
    stdate = zigzag_xdata[-3]
    endate = zigzag_xdata[-2]
    CN1 = getcandnum(df, Fdata, Edata, st_date, end_date)

    Fdata = zigline[-2]
    Edata = zigline[-1]
    stdate = zigzag_xdata[-2]
    endate = zigzag_xdata[-1]
    CN2 = getcandnum(df, Fdata, Edata, st_date, end_date)

    if CN1 + CN2 > 4:
        upcont = 1
        dncont = 1
        maxbarcontup = 1
        maxbarcontdn = glbarcount

        rangedataup = [currhigh, currlow]
        rangedatadn = [currhigh, currlow]

        zigvariable['maxbarcontup'] = maxbarcontup
        zigvariable['maxbarcontdn'] = maxbarcontdn
        zigvariable['upcont'] = upcont
        zigvariable['dncont'] = dncont
        zigvariable['rangedataup'] = rangedataup
        zigvariable['rangedatadn'] = rangedatadn

    else:
        rangedataup = [currhigh, rangedataup[1]]
        zigvariable['rangedataup'] = rangedataup

    TOTALMOVE = list(zigline[-1].values())[0][1] - \
                list(zigline[-2].values())[0][1]
    dnmov = list(zigline[-1].values())[0][1] - TOTALMOVE * permv

    zigvariable['gppoint'] = gppoint
    zigvariable['zigline'] = zigline
    zigvariable['zigzag_ydata'] = zigzag_ydata
    zigvariable['zigzag_xdata'] = zigzag_xdata
    zigvariable['canlen'] = canlen
    zigvariable['dnmov'] = dnmov

    return zigvariable
def rule4_1_dnmove(count, index, zigvariable, df):
    rangedata = zigvariable['rangedata']
    rangedataup = zigvariable['rangedataup']
    rangedatadn = zigvariable['rangedatadn']
    upmov = zigvariable['upmov']
    dnmov = zigvariable['dnmov']
    upcont = zigvariable['upcont']
    dncont = zigvariable['dncont']

    secupcont = zigvariable['secupcont']
    secdncont = zigvariable['secdncont']
    gppoint = zigvariable['gppoint']
    zigline = zigvariable['zigline']
    zigzag_ydata = zigvariable['zigzag_ydata']
    zigzag_xdata = zigvariable['zigzag_xdata']
    canlen = zigvariable['canlen']
    index_list_count = zigvariable['index_list_count']

    currhigh = zigvariable['currhigh']
    currlow = zigvariable['currlow']
    seconlastcheck = zigvariable['seconlastcheck']
    maxbarcontdn = zigvariable['maxbarcontdn']
    maxbarcontup = zigvariable['maxbarcontup']
    permv = zigvariable['permv']
    glbarcount = zigvariable['glbarcount']


    maxcheck = min(7, len(zigline) - 1)
    # print(maxcheck)
    foundid = 0
    for CIIL, check_candel in enumerate(reversed(zigline)):
        cand_num = list(check_candel.keys())[0]
        cand_value = list(check_candel.values())[0]
        # print(cand_num, cand_value)

        if cand_value[1] < currlow and cand_value[0] == -1:
            foundid = 1
            # print('found at', CIIL)
            # print('zigline00==', zigline)
            break

        if CIIL > maxcheck:
            break


    if foundid == 0:
        # print(zigline)
        # print(maxcheck)

        check_L_L = list(list(reversed(zigline))[maxcheck].values())[0][0]
        if check_L_L == 1:
            maxcheck = maxcheck - 1

        # dfg
        # st_p=list(reversed(zigline))[maxcheck]
        # end_p=zigline[-1]

        st_date = list(reversed(zigzag_xdata))[maxcheck]
        end_date = index

        Sdate_indexN = df.index.get_loc(st_date)
        Edate_indexN = df.index.get_loc(end_date)

        #
        #                     # print(st_p,end_p)
        #                     # print(st_date, end_date)
        #                     # print(Sdate_indexN,Edate_indexN)

        subdf = df.loc[st_date:end_date]
        #                     # print(subdf)

        high_value = subdf.loc[:, 'high'].max()
        high_valuedate = subdf.loc[:, 'high'].idxmax()
        # print(high_value, high_valuedate)

        count_high = index_list_count[high_valuedate]
        # print('AA=', high_value, high_valuedate, count_high)

        # print(zigline)

        for C1, lastlow in enumerate(reversed(zigline)):
            can1_num = list(lastlow.keys())[0]
            cand1_value = list(lastlow.values())[0]
            # print(can1_num, cand1_value)
            if can1_num < count_high and cand1_value[0] == -1:
                CII = C1
                st_date = list(reversed(zigzag_xdata))[C1]
                break

        subdf2 = subdf.loc[st_date:high_valuedate, :]
        # # print(subdf2)
        # print(high_valuedate)

        # CH_HIGH = subdf2.iloc[0, 1]
        CH_HIGH = subdf2.iloc[0, subdf2.columns.get_loc("high")]
        #                     # print(CH_LOW)
        # subdf2.loc[subdf2['low'] < CH_LOW, 'CHECK LOW'] = 1
        # subdf2.loc[subdf2['low'] >= CH_LOW, 'CHECK LOW'] = 0
        subdf2.loc[
            subdf2.loc[:, 'high'] > CH_HIGH, 'CHECK HIGH'] = 1
        subdf2.loc[
            subdf2.loc[:, 'high'] <= CH_HIGH, 'CHECK HIGH'] = 0

        #                     # print(subdf2)

        Total_high_cand = int(subdf2.loc[:, 'CHECK HIGH'].sum()) + 1
        #                     # print(Total_low_cand)

        CNT1 = Total_high_cand
        xdata = high_valuedate

        count_high = index_list_count[high_valuedate]

        CIIL = C1




    else:
        # llc = df.index.get_loc(low_date)

        # st_p = list(reversed(zigline))[CII]
        # end_p = zigline[-1]

        st_date = list(reversed(zigzag_xdata))[CIIL]
        end_date = index

        Sdate_indexN = df.index.get_loc(st_date)
        Edate_indexN = df.index.get_loc(end_date)

        #
        # # print(st_p,end_p)
        # print(st_date, end_date)
        # print(Sdate_indexN, Edate_indexN)

        subdf = df.loc[st_date:end_date, :]
        #                     # print(subdf)

        high_value = subdf.loc[:, 'high'].max()
        high_valuedate = subdf.loc[:, 'high'].idxmax()
        # print(high_value, high_valuedate)

        subdf4 = subdf.loc[st_date:high_valuedate, :]
        # # print(subdf2)
        # print(high_valuedate)

        CH_HIGH = subdf4.iloc[0, subdf4.columns.get_loc("high")]
        # print('CH_HIGH',CH_HIGH)
        subdf4.loc[subdf4.loc[:, 'high'] > CH_HIGH, 'CHECK HIGH'] = 1
        subdf4.loc[subdf4.loc[:, 'high'] <= CH_HIGH, 'CHECK HIGH'] = 0

        #                     # print(subdf2)

        Total_high_cand = int(subdf4.loc[:, 'CHECK HIGH'].sum()) + 1
        #                     # print(Total_low_cand)

        CNT1 = Total_high_cand
        xdata = high_valuedate
        count_high = index_list_count[high_valuedate]

        CIIL = CIIL

    if len(gppoint) > 2:
        gppoint = gppoint[: len(gppoint) - CIIL]
        zigline = zigline[: len(zigline) - CIIL]
        canlen = canlen[: len(canlen) - CIIL]
        zigzag_ydata = zigzag_ydata[: len(zigzag_ydata) - CIIL]
        zigzag_xdata = zigzag_xdata[: len(zigzag_xdata) - CIIL]

    h_point = {count_high: [1, high_value]}

    gppoint.append(h_point)
    zigline.append(h_point)
    zigzag_ydata.append(high_value)
    zigzag_xdata.append(xdata)
    canlen.append(([1, CNT1, high_value]))

    dnpoint = {count: [-1, currlow]}

    secdncont = secdncont + 1
    zigvariable['secdncont'] = secdncont

    gppoint.append(dnpoint)
    zigline.append(dnpoint)
    zigzag_ydata.append(currlow)
    zigzag_xdata.append(index)

    # canlen[-1] = list(zigline[-1].keys())[0] - list(zigline[-2].keys())[0]
    canlen.append(([-1, secdncont, currlow]))

    Fdata = zigline[-3]
    Edata = zigline[-2]
    stdate = zigzag_xdata[-3]
    endate = zigzag_xdata[-2]
    CN1 = getcandnum(df, Fdata, Edata, st_date, end_date)

    Fdata = zigline[-2]
    Edata = zigline[-1]
    stdate = zigzag_xdata[-2]
    endate = zigzag_xdata[-1]
    CN2 = getcandnum(df, Fdata, Edata, st_date, end_date)

    if CN1 + CN2 > 4:
        upcont = 1
        dncont = 1
        maxbarcontup = glbarcount
        maxbarcontdn = 1

        rangedataup = [currhigh, currlow]
        rangedatadn = [currhigh, currlow]

        zigvariable['maxbarcontup'] = maxbarcontup
        zigvariable['maxbarcontdn'] = maxbarcontdn
        zigvariable['upcont'] = upcont
        zigvariable['dncont'] = dncont
        zigvariable['rangedataup'] = rangedataup
        zigvariable['rangedatadn'] = rangedatadn

    else:

        rangedatadn = [rangedatadn[0], currlow]
        zigvariable['rangedatadn'] = rangedatadn



    TOTALMOVE = list(zigline[-2].values())[0][1] - \
                list(zigline[-1].values())[0][1]
    upmov = list(zigline[-1].values())[0][1] + TOTALMOVE * permv

    zigvariable['gppoint'] = gppoint
    zigvariable['zigline'] = zigline
    zigvariable['zigzag_ydata'] = zigzag_ydata
    zigvariable['zigzag_xdata'] = zigzag_xdata
    zigvariable['canlen'] = canlen
    zigvariable['upmov'] = upmov

    return zigvariable
def HL_LL_LH_HH(df, zigzag_xdata, zigzag_ydata, index_list_count, zigline):

    zig_df = df.copy()
    # zig_df=pd.DataFrame(index=df.index)
    new_d = pd.Series(index_list_count)

    # print(index_list_count)


    zigline_dict = {}
    for data1, data2 in zip(zigzag_xdata, zigzag_ydata):
        zigline_dict.update({data1: data2})

    zig_ind_dict = {}
    for ID, data1 in enumerate(zigline):
        c1 = list(data1.keys())[0]
        d1 = int(list(data1.values())[0][0])
        zig_ind_dict.update({c1: d1})

    zig_df['count'] = zig_df.index.map(index_list_count)
    zig_df['zigzagvalue'] = zig_df.index.map(zigline_dict)
    zig_df['zigindex'] = zig_df['count'].map(zig_ind_dict)

    temp_array = []
    temp_text_array = {}
    temp_regection_array = {}
    #     # print(zigline)
    for ID, data1 in enumerate(zigline):
        c1 = list(data1.keys())[0]
        d1 = int(list(data1.values())[0][0])
        temp_array.append(c1)

        if ID == 0:
            temp_text_array.update({c1: 'B'})
        if ID == 1:
            if d1 == 1:
                temp_text_array.update({c1: 'H'})
            else:
                temp_text_array.update({c1: 'L'})
        if ID == 2:
            if d1 == 1:
                temp_text_array.update({c1: 'H'})
            else:
                temp_text_array.update({c1: 'L'})

        if ID > 2:
            # print(ID, data1)
            current_candle = zig_df.loc[zig_df['count'] == temp_array[-1]]
            previous_candle = zig_df.loc[zig_df['count'] == temp_array[-3]]
            hltext, regect_can = check_high_low(current_candle, previous_candle)
            temp_text_array.update({c1: hltext})
            temp_regection_array.update({c1: regect_can})

    zig_df['zigzagtext'] = zig_df['count'].map(temp_text_array)
    zig_df['rejectioncandel'] = zig_df['count'].map(temp_regection_array)
    zig_df['zigzagline'] = zig_df.loc[:, 'zigzagvalue'].interpolate()

    # return zig_df[['count','high','low','zigindex','zigzagvalue','zigzagtext','rejectioncandel','zigzagline']]
    return zig_df
def check_high_low(current_candle, previous_candle):

    # print('@@@@@')
    # print('current_candle',current_candle)
    # print('previous_candle',previous_candle)
    # print('@@@@@')

    if current_candle.iloc[0]['zigindex'] == 1 and previous_candle.iloc[0][
        'zigindex'] == 1:
        #         # print('high regin')

        if current_candle.iloc[0]['close'] > previous_candle.iloc[0]['high']:
            htext = 'HH'
            regec = 0
        elif current_candle.iloc[0]['close'] <= previous_candle.iloc[0][
            'high'] and current_candle.iloc[0]['high'] >= \
                previous_candle.iloc[0]['high']:
            htext = 'H'
            regec = 1
        elif current_candle.iloc[0]['high'] < previous_candle.iloc[0]['high']:
            htext = 'LH'
            regec = 0
        else:
            checkhere


    elif current_candle.iloc[0]['zigindex'] == -1 and previous_candle.iloc[0][
        'zigindex'] == -1:
        #         # print('low regin')

        if current_candle.iloc[0]['close'] < previous_candle.iloc[0]['low']:
            htext = 'LL'
            regec = 0
        elif current_candle.iloc[0]['close'] >= previous_candle.iloc[0][
            'low'] and current_candle.iloc[0]['low'] <= previous_candle.iloc[0][
            'low']:
            htext = 'L'
            regec = -1
        elif current_candle.iloc[0]['low'] > previous_candle.iloc[0]['low']:
            htext = 'HL'
            regec = 0
        else:
            checkhere

    else:
        htext = 'C'
        regec = 0

    return htext, regec


def getcandnum(df, Fdata, Edata, st_date, end_date):
    subdf3 = df.loc[st_date:end_date, :]

    if list(Fdata.values())[0][0] == 1 and list(Edata.values())[0][0] == -1:
        low_value = subdf3.loc[:, 'low'].min()
        low_valuedate = subdf3.loc[:, 'low'].idxmin()
        #         # print(low_value, low_valuedate)

        subdf4 = subdf3.loc[st_date:low_valuedate, :]

        # CH_LOW = subdf4.iloc[0, 3]
        CH_LOW = subdf4.iloc[0, subdf4.columns.get_loc("low")]

        low_lit = subdf4['low'].to_list()

        temp_laray = []

        for ix, lw in enumerate(low_lit):
            if ix == 0:
                temp_laray.append(lw)
            elif lw < temp_laray[-1]:
                temp_laray.append(lw)
            else:
                pass
        Total_low_cand = len(temp_laray)

        CNT1 = Total_low_cand
        xdata = low_valuedate
    else:
        high_value = subdf3.loc[:, 'high'].max()
        high_valuedate = subdf3.loc[:, 'high'].idxmax()
        #         # print(high_value, high_valuedate)

        subdf4 = subdf3.loc[st_date:high_valuedate, :]

        # CH_High = subdf4.iloc[0, 1]
        CH_High = subdf4.iloc[0, subdf4.columns.get_loc("open")]

        high_lit = subdf4['high'].to_list()

        temp_laray = []

        for ix, lw in enumerate(high_lit):
            if ix == 0:
                temp_laray.append(lw)
            elif lw > temp_laray[-1]:
                temp_laray.append(lw)
            else:
                pass
        Total_high_cand = len(temp_laray)

        CNT1 = Total_high_cand
        xdata = high_valuedate

    return CNT1
def cal_hzig_lines(zig_df):
# # #     # print(zig_df)
    HH_L = zig_df.loc[zig_df['zigzagtext'] == 'HH']
    H = zig_df.loc[zig_df['zigzagtext'] == 'H']
    H_RL = zig_df.loc[zig_df['rejectioncandel'] == 1]

    LL_L = zig_df.loc[zig_df['zigzagtext'] == 'LL']
    L_RL = zig_df.loc[zig_df['rejectioncandel'] == -1]

    break_candel=[]
    ### FOR HH LINE
    HH_LIST = HH_L['high'].to_list()
    HH_CON = HH_L['count'].to_list()


    HH_LIST_add = H['high'].to_list()
    HH_CON_add = H['count'].to_list()
    HH_LIST.extend(HH_LIST_add)
    HH_CON.extend(HH_CON_add)



    valid_HH = {}
    LINE_COORDINX = []
    LINE_COORDINY = []
    allvalid_zig_HZ_trendlines={}

    zig_HH_trend_list={}
    for ind, hh_value in enumerate(HH_LIST):
        IND = 1
        high_candle=HH_CON[ind]
        break_candel, IND = getbreakcandel2(zig_df, high_candle, hh_value, HH_CON, break_candel, IND, check_side='HIGC')
        # print('break_candel==',break_candel,IND)
        if len(break_candel)>0:
            # print(zig_df)
            linecross_IND, linecross_can = check_cross_hz_line(zig_df, break_candel[0], check_side='HIGC')
        else:
            # linecross_IND=2
            linecross_IND, linecross_can = check_cross_hz_line(zig_df, high_candle, check_side='HIGC')

        zig_HH_trend_list.update({high_candle: [break_candel,linecross_IND]})
    # print(zig_HH_trend_list)

    allvalid_zig_HZ_trendlines.update({'HH': zig_HH_trend_list})



    ### FOR H_RL LINE
    HH_LIST = H_RL['high'].to_list()
    HH_CON = H_RL['count'].to_list()
    valid_HRL = {}
    zig_HRH_trend_list={}
    for ind, hh_value in enumerate(HH_LIST):
        high_candle=HH_CON[ind]
        IND = 1
        high_candle = HH_CON[ind]
        break_candel, IND = getbreakcandel2(zig_df, high_candle, hh_value, HH_CON, break_candel, IND, check_side='HIGC')
#         # print('break_candel==',break_candel,IND)
        if len(break_candel) > 0:
            linecross_IND, linecross_can = check_cross_hz_line(zig_df, break_candel[0], check_side='HIGC')
        else:
            linecross_IND, linecross_can = check_cross_hz_line(zig_df, high_candle, check_side='HIGC')

        zig_HRH_trend_list.update({high_candle: [break_candel, linecross_IND]})

    # print(zig_HRH_trend_list)

    allvalid_zig_HZ_trendlines.update({'HRL': zig_HRH_trend_list})


    ### FOR LL LINE
    LL_LIST = LL_L['low'].to_list()
    LL_CON = LL_L['count'].to_list()
    valid_LL = {}
# # #     # print(LL_LIST)
# # #     # print(LL_CON)
    zig_LL_trend_list={}
    for ind, ll_value in enumerate(LL_LIST):
        low_candle = LL_CON[ind]
        IND = 1
        break_candel, IND = getbreakcandel2(zig_df, low_candle, ll_value, LL_CON, break_candel, IND, check_side='LOWC')
#         # print('break_candel==', break_candel, IND)
        if len(break_candel)>0:
            linecross_IND, linecross_can = check_cross_hz_line(zig_df, break_candel[0], check_side='LOWC')
        else:
            linecross_IND, linecross_can = check_cross_hz_line(zig_df, low_candle, check_side='LOWC')

        zig_LL_trend_list.update({low_candle: [break_candel,linecross_IND]})

    # print(zig_LL_trend_list)
    allvalid_zig_HZ_trendlines.update({'LL': zig_LL_trend_list})

    ### FOR L_RL LINE
    LL_LIST = L_RL['low'].to_list()
    LL_CON = L_RL['count'].to_list()
# # #     # print(LL_LIST)
# # #     # print(LL_CON)
    valid_LRL = {}
    zig_LRL_trend_list={}
    for ind, ll_value in enumerate(LL_LIST):
        low_candle= LL_CON[ind]
        IND = 1
        break_candel, IND = getbreakcandel2(zig_df, low_candle, ll_value, LL_CON, break_candel, IND, check_side='LOWC')
#         # print('break_candel==', break_candel, IND)
        if len(break_candel) > 0:
            linecross_IND, linecross_can = check_cross_hz_line(zig_df, break_candel[0], check_side='LOWC')
        else:
            linecross_IND, linecross_can = check_cross_hz_line(zig_df, low_candle, check_side='LOWC')

        zig_LRL_trend_list.update({low_candle: [break_candel, linecross_IND]})


    # print(zig_LRL_trend_list)

    allvalid_zig_HZ_trendlines.update({'LRL': zig_LRL_trend_list})
    # print(allvalid_zig_HZ_trendlines)


    return allvalid_zig_HZ_trendlines
def getbreakcandel2(zig_df,strat_candle_count, strat_candle_value,HL_LIST,break_candel,IND,check_side='HIGC'):

    HHLL_LIST = HL_LIST.copy()
    HHLL_LIST.insert(len(HHLL_LIST), 10000)

    # print(HHLL_LIST)
    next_index = next(x[0] for x in enumerate(HHLL_LIST) if x[1] > strat_candle_count)
    next_value = HHLL_LIST[next_index]
#     # print('next_value', HHLL_LIST[next_index])

    # break_candel = []
    if check_side == "LOWC":
        conditions = [(zig_df.iloc[strat_candle_count:]['close'] < strat_candle_value)]

    if check_side == "HIGC":
        conditions = [(zig_df.iloc[strat_candle_count:]['close'] > strat_candle_value)]

    choices = [zig_df.iloc[strat_candle_count:]['count']]

    temp_array = np.select(conditions, choices, default=np.nan)
    te_arr = np.unique(temp_array[~np.isnan(temp_array)])
    CH = len(np.unique(temp_array[~np.isnan(temp_array)]))
    CHNAN = np.argwhere(np.isnan(temp_array))

#     # print(temp_array)
#     # print(te_arr)
    # rejct_candle = []
    # IND=1

    while IND==1:
        if len(CHNAN) < len(temp_array):
            first_canbreak = int(te_arr[0])
#             # print(first_canbreak, next_value)

            if first_canbreak > next_value:
                break_candel = []
                # T=0
                # print('no rejection found and no break up ')
                # return break_candel
                IND=0
                break

#             # print('strat_candle_count=', strat_candle_count, 'first_canbreak=', first_canbreak)
            if check_side == "LOWC":
                rejct_candle = check_bweteen_rejection(strat_candle_count, first_canbreak, zig_df, 'LOW')
            if check_side == "HIGC":
                rejct_candle = check_bweteen_rejection(strat_candle_count, first_canbreak, zig_df, 'HIGH')

#             # print('rejct_candle==', rejct_candle)
            if len(rejct_candle) == 1:
                break_candel = [strat_candle_count, first_canbreak]
                IND = 0
                break
                # return break_candel

            if len(rejct_candle) > 1:
#                 # print('rejc=', rejct_candle[0], 'oldbearl_can=', rejct_candle[1], check_side)

                if check_side == "HIGC":
                    strat_candle_value = zig_df.loc[zig_df['count'] == rejct_candle[0], 'high'].iloc[0]
                    break_candel,IND = getbreakcandel2(zig_df, rejct_candle[0], strat_candle_value, HL_LIST,break_candel,IND, 'HIGC')
#                     # print('AAAA=', break_candel)

                if check_side == "LOWC":
                    strat_candle_value = zig_df.loc[zig_df['count'] == rejct_candle[0], 'low'].iloc[0]
                    break_candel,IND = getbreakcandel2(zig_df, rejct_candle[0], strat_candle_value, HL_LIST,break_candel,IND, 'LOWC')
#                     # print('BBBB=', break_candel)

            else:
                break_candel = [strat_candle_count, first_canbreak]
                # print('no rejection found and return break at ', break_candel)
                # break_candel = ['yess']
#                 # print(break_candel)
                IND = 0
                break

                # return break_candel
        else:
            # # print(break_candel)
            # print('no value found for')
            break_candel=[]
            IND = 0
            break

#     # print(break_candel,IND)

    return break_candel,IND
def in_ist(small_list, big_list):
    return ''.join(str(x) for x in small_list) in ''.join(
        str(y) for y in big_list)
def check_bweteen_rejection(first_candle,last_candle,zpd,check_parameter):
# # #     # print(first_candle, last_candle)
    # sundf=zig_df.
    newcandleline=[last_candle]

    subdf=zpd.loc[(zpd['count'] > first_candle) & (zpd['count'] < last_candle)]
# # #     # print(subdf)

    if check_parameter=='LOW':
        lvalue=zpd.loc[zpd['count'] == first_candle, 'low'].iloc[0]
        subdf2 = subdf.loc[(subdf['low']<lvalue)]
# # #         # print(subdf2)

        if subdf2.shape[0] != 0:
            if subdf2.shape[0]>1:
                newlowcandle = subdf2.loc[subdf2['low'].idxmin()]['count']
                newcandleline.insert(0, newlowcandle)
            else:
                newlowcandle=subdf2.loc[:,'count'].tolist()[0]
                # ll_value = subdf2.loc[:, 'low'].tolist()[0]
                newcandleline.insert(0, newlowcandle)
# # #                 # print(newcandleline)

    if check_parameter == 'HIGH':
        hvalue = zpd.loc[zpd['count'] == first_candle, 'high'].iloc[0]
        subdf2 = subdf.loc[(subdf['high'] > hvalue)]
# # #         # print(subdf2)

        if subdf2.shape[0]!=0:
            if subdf2.shape[0] > 1:
#                 # print(hvalue)
#                 # print(subdf2)
                newlowcandle=subdf2.loc[subdf2['high'].idxmax()]['count']
                newcandleline.insert(0, newlowcandle)
#                 # print(newlowcandle)
                # help1
            else:
                newlowcandle = subdf2.loc[:, 'count'].tolist()[0]
                # hh_value = subdf2.loc[:, 'high'].tolist()[0]
                newcandleline.insert(0, newlowcandle)
# # #                 # print(newcandleline)



# # #         # print(lvalue)
    return newcandleline
def tend_segment(zig_df):
    # Lin_ind_HH = zig_df.loc[zig_df['zigzagtext'] == 'HH']['count']
    # Lin_ind_HL = zig_df.loc[zig_df['zigzagtext'] == 'HL']['count']
    AA = np.argwhere(zig_df['zigzagtext'].notnull().values).tolist()
    # BB=list(zig_df[zig_df['zigzagtext'].notnull()].stack()['zigzagtext'])
    filderdf = zig_df[zig_df['zigzagtext'].notnull()]
    filder_HL0 = filderdf[['count', 'zigzagtext']]
    filder_HL = filder_HL0.to_dict('index')

# # #     # print(filderdf)


    # count_HL = filderdf['count'].to_list()
    # text_HL = filderdf['zigzagtext'].to_list()
# # #     # print(text_HL)

    # filder_HL.to_dict('dict')
    # F2=filder_HL.index.T.to_dict('list')
    #

    # HH_LIST = HH_L['high'].to_list()
# # #     # print(filder_HL)
# # #     # print(F2)
    uptrend1 = ['HH', 'HL']
    uptrend2 = ['HL', 'HH']
    uptrend3 = ['LL', 'HH']
    uptrend4 = ['L', 'HH']


    lowtrend1 = ['LL', 'LH']
    lowtrend2 = ['LH', 'LL']

    temp_array1 = []
    temp_array2 = []

    zig_df["zigtrendp"] = ''

    for II in filder_HL.items():
# # #         # print(II)
# # #         # print(II[0])
# # #         # print(II[1]['count'])
# # #         # print(II[1]['zigzagtext'])
        temp_text = II[1]['zigzagtext']
        temp_cont = II[1]['count']
        if len(temp_array1) <= 2:
            temp_array1.append(temp_text)
            temp_array2.append(temp_cont)
# # #             # print(temp_array2)
            if len(temp_array1) == 2:
# # #                 # print(temp_array1)
# # #                 # print(temp_array2)

                UPBOOL1=in_ist(uptrend1, temp_array1)
                UPBOOL2 = in_ist(uptrend2, temp_array1)
                UPBOOL3 = in_ist(uptrend3, temp_array1)
                UPBOOL4 = in_ist(uptrend4, temp_array1)

                DNBOOL1 = in_ist(lowtrend1, temp_array1)
                DNBOOL2 = in_ist(lowtrend2, temp_array1)

                if UPBOOL1==True or UPBOOL2==True or UPBOOL3==True or UPBOOL4==True:
                    zig_df.loc[(zig_df['count'] >= temp_array2[0]) & (zig_df['count'] <= temp_array2[1]), 'zigtrendp'] = 'green'
                elif DNBOOL1==True or DNBOOL2==True:
                   zig_df.loc[(zig_df['count'] >= temp_array2[0]) & (zig_df['count'] <= temp_array2[1]), 'zigtrendp'] = 'red'
                else:
                    zig_df.loc[(zig_df['count'] >= temp_array2[0]) & (zig_df['count'] <= temp_array2[1]), 'zigtrendp'] = 'black'

                temp_array1.pop(0)
                temp_array2.pop(0)

# # #     # print(zig_df)


    blc = zig_df.loc[zig_df['zigtrendp'] == 'black']
    blc_list= blc['count'].to_list()
# # #     # print(blc_list)
    bl_list=[]
    con=0
    for indx,val in enumerate(blc_list[0:-1]):
# # #         # print(len(blc_list),indx,val)
        if indx==0:
            bl_list.append(val)

        if val+1==blc_list[indx+1]:
# # #             # print('con')
            con=1
            if len(bl_list) % 2 == 0:
                bl_list.append(val)
        else:
            if len(bl_list) % 2 != 0:
                con = 0
                bl_list.append(val)
# # #             # print('miss')

    if con==1:
        bl_list.append(blc_list[-1])

# # #     # print(bl_list)

    grn = zig_df.loc[zig_df['zigtrendp'] == 'green']

    grn_list = grn['count'].to_list()
# # #     # print(grn_list)
    gn_list = []
    con = 0
    for indx, val in enumerate(grn_list[0:-1]):
# # #         # print(len(blc_list),indx,val)
        if indx == 0:
            gn_list.append(val)

        if val + 1 == grn_list[indx + 1]:
# # #             # print('con')
            con = 1
            if len(gn_list) % 2 == 0:
                gn_list.append(val)
        else:
            if len(gn_list) % 2 != 0:
                con = 0
                gn_list.append(val)
# # #             # print('miss')

    if con == 1:
        gn_list.append(grn_list[-1])

# # #     # print(gn_list)

    renl = zig_df.loc[zig_df['zigtrendp'] == 'red']

    renl_list = renl['count'].to_list()
# # #     # print(renl_list)

    rn_list = []
    con = 0
    for indx, val in enumerate(renl_list[0:-1]):
# # #         # print(len(blc_list),indx,val)
        if indx == 0:
            rn_list.append(val)

        if val + 1 == renl_list[indx + 1]:
# # #             # print('con')
            con = 1
            if len(rn_list) % 2 == 0:
                rn_list.append(val)
        else:
            if len(rn_list) % 2 != 0:
                con = 0
                rn_list.append(val)
# # #             # print('miss')

    if con == 1:
        rn_list.append(renl_list[-1])

# # #     # print(rn_list)
    # uloi

    itb = iter(bl_list)
    itg = iter(gn_list)
    itr= iter(rn_list)



    sid_lic_cor={}
    cont=1
    for a in itb:
        b = next(itb)
        x1=zig_df.index[zig_df['count'] == a].tolist()
        x2 = zig_df.index[zig_df['count'] == b].tolist()
# # #         # print(x1)
        # ffgh
        sid_lic_cor.update({cont:[x1[0],x2[0]]})
        cont=cont+1


    up_lic_cor = {}
    cont = 1
    for a in itg:
        b = next(itg)
        x1 = zig_df.index[zig_df['count'] == a].tolist()
        x2 = zig_df.index[zig_df['count'] == b].tolist()
# # #         # print(x1)
        # ffgh
        up_lic_cor.update({cont: [x1[0], x2[0]]})
        cont = cont + 1

    dn_lic_cor = {}
    cont = 1
    for a in itr:
        b = next(itr)
        x1 = zig_df.index[zig_df['count'] == a].tolist()
        x2 = zig_df.index[zig_df['count'] == b].tolist()
# # #         # print(x1)
        # ffgh
        dn_lic_cor.update({cont: [x1[0], x2[0]]})
        cont = cont + 1

    # print(sid_lic_cor)
    # print(up_lic_cor)
    # print(dn_lic_cor)

    trend_list=[sid_lic_cor,up_lic_cor,dn_lic_cor]





    return trend_list
def check_cross_hz_line(zig_df,strat_candle_count,check_side='HIGC'):
    # print('strat_candle_count',strat_candle_count)
    if check_side=='LOWC':
        strat_candle_low = zig_df.loc[zig_df['count'] == strat_candle_count, 'low'].tolist()[0]

    if check_side=='HIGC':
        strat_candle_low1 = zig_df.loc[zig_df['count'] == strat_candle_count, 'high']
        # print(strat_candle_low1)
        strat_candle_low = zig_df.loc[zig_df['count'] == strat_candle_count, 'high'].tolist()[0]


    linecross=0
    inecrosscandle=0
    conditions = [
        (zig_df.iloc[strat_candle_count:]['close'] > strat_candle_low) & (
                zig_df.iloc[strat_candle_count:]['open'] < strat_candle_low),
        (zig_df.iloc[strat_candle_count:]['close'] < strat_candle_low) & (
                zig_df.iloc[strat_candle_count:]['open'] > strat_candle_low)]

    choices = [zig_df.iloc[strat_candle_count:]['count'],
               zig_df.iloc[strat_candle_count:]['count']]

    temp_array = np.select(conditions, choices, default=np.nan)
    te_arr = np.unique(temp_array[~np.isnan(temp_array)])
    CH = len(np.unique(temp_array[~np.isnan(temp_array)]))
    CHNAN = np.argwhere(np.isnan(temp_array))

    if CH == 1 or len(CHNAN) == len(temp_array):
        if CH == 1:
            linecross=1
            inecrosscandle=int(te_arr[0])
        if len(CHNAN) == len(temp_array):
            linecross = 2
            inecrosscandle = strat_candle_count

    return linecross,inecrosscandle
def  cal_breakup(zig_df,allvalid_zig_HZ_trendlines):
    # print(allvalid_zig_HZ_trendlines)
    valid_breakup_price={}
    valid_breakdn_price = {}

    for tline, tlist in allvalid_zig_HZ_trendlines.items():
        x_data = []
        y_data = []
#         # print('tlist',tline,tlist)

        if tline == 'HH' or tline == 'HRL':
            for IN, L1 in enumerate(reversed(tlist)):
#                 # print('L1==',L1)
                if len(tlist[L1][0]) > 0:
                    if L1!=tlist[L1][0][-1]:
                        brekcand=tlist[L1]
#                         # print('brekcand',brekcand)
                        valid_breakup_price.update({L1:tlist[L1][0][-1]})

        if tline == 'LL' or tline == 'LRL':
            for IN, L1 in enumerate(reversed(tlist)):
                if len(tlist[L1][0])>0:
                    if L1!=tlist[L1][0][-1]:
                        brekcand=tlist[L1]
#     # #                     # print(brekcand)
                        valid_breakdn_price.update({L1:tlist[L1][0][-1]})

    return valid_breakup_price, valid_breakdn_price

    
def  cal_breakup0(fig,zig_df,allvalid_zig_HZ_trendlines):
    # print(allvalid_zig_HZ_trendlines)
    valid_breakup_price={}
    valid_breakdn_price = {}

    for tline, tlist in allvalid_zig_HZ_trendlines.items():
        x_data = []
        y_data = []
#         # print('tlist',tline,tlist)

        if tline == 'HH' or tline == 'HRL' or tline == 'H':
            for IN, L1 in enumerate(reversed(tlist)):
#                 # print('L1==',L1)
                if len(tlist[L1][0]) > 0:
                    if L1!=tlist[L1][0][-1]:
                        brekcand=tlist[L1]
#                         # print('brekcand',brekcand)
                        valid_breakup_price.update({L1:tlist[L1][0][-1]})

        if tline == 'LL' or tline == 'LRL':
            for IN, L1 in enumerate(reversed(tlist)):
                if len(tlist[L1][0])>0:
                    if L1!=tlist[L1][0][-1]:
                        brekcand=tlist[L1]
#     # #                     # print(brekcand)
                        valid_breakdn_price.update({L1:tlist[L1][0][-1]})

    # print(valid_breakup_price)
    # print(valid_breakdn_price)

    for speccand in valid_breakup_price.values():
# # #         # print(speccand)

        x_data = zig_df.index[zig_df['count'] == speccand].tolist()[0]
        high = zig_df.loc[zig_df['count'] == speccand, 'high'].iloc[0]
        low=   zig_df.loc[zig_df['count'] == speccand, 'low'].iloc[0]
        open = zig_df.loc[zig_df['count'] == speccand, 'open'].iloc[0]
        close = zig_df.loc[zig_df['count'] == speccand, 'close'].iloc[0]
# # #         # print(x_data,high,open,close,low)

        track_highlight = fig.add_trace(go.Candlestick(
            x=[x_data],
            open=[open],
            high=[high],
            low=[low],
            close=[close],
            increasing={'line': {'color': 'purple'}},
            decreasing={'line': {'color': 'purple'}},
            name='highlight'))

    for speccand in valid_breakdn_price.values():
# # #         # print(speccand)

        x_data = zig_df.index[zig_df['count'] == speccand].tolist()[0]
        high = zig_df.loc[zig_df['count'] == speccand, 'high'].iloc[0]
        low=   zig_df.loc[zig_df['count'] == speccand, 'low'].iloc[0]
        open = zig_df.loc[zig_df['count'] == speccand, 'open'].iloc[0]
        close = zig_df.loc[zig_df['count'] == speccand, 'close'].iloc[0]
# # #         # print(x_data,high,open,close,low)

        track_highlight = fig.add_trace(go.Candlestick(
            x=[x_data],
            open=[open],
            high=[high],
            low=[low],
            close=[close],
            increasing={'line': {'color': 'black'}},
            decreasing={'line': {'color': 'black'}},
            name='highlight'))




    # highlight_inds = [1, 3]
    # track_highlight = go.Candlestick(
    #     x=[dates[i] for i in highlight_inds],
    #     open=[open_data[i] for i in highlight_inds],
    #     high=[high_data[i] for i in highlight_inds],
    #     low=[low_data[i] for i in highlight_inds],
    #     close=[close_data[i] for i in highlight_inds],
    #     increasing={'line': {'color': 'yellow'}},
    #     decreasing={'line': {'color': 'purple'}},
    #     name='highlight'
    # )
