from collections import Counter
import pandas as pd
import requests
from tqdm import tqdm
import json

drwtNo1 = []
drwtNo2 = []
drwtNo3 = []
drwtNo4 = []
drwtNo5 = []
drwtNo6 = []
bnusNo = []
totSellamnt = []
drwNoDate = []
firstAccumamnt = []
firstPrzwnerCo = []
firstWinamnt = []

MaxDrwNo = 1000
count = 0

def getLottoWinInfo(minDrwNo, cnt):
    #tqdm -> 반복문이 얼만큼 진행 됐는지 표시하는 진행표시바

    i = minDrwNo
    while True:          
        req_url = "https://www.dhlottery.co.kr/common.do?method=getLottoNumber&drwNo=" + str(i)

        req_lotto = requests.get(req_url)
        lottoNo = req_lotto.json()

        if lottoNo['returnValue'] == 'fail':
            break

        drwtNo1.append(lottoNo['drwtNo1'])      #1~6번째 번호
        drwtNo2.append(lottoNo['drwtNo2'])
        drwtNo3.append(lottoNo['drwtNo3'])
        drwtNo4.append(lottoNo['drwtNo4'])
        drwtNo5.append(lottoNo['drwtNo5'])
        drwtNo6.append(lottoNo['drwtNo6'])
        bnusNo.append(lottoNo['bnusNo'])        #보너스 번호

        totSellamnt.append(lottoNo['totSellamnt'])  #총 판매금액
        drwNoDate.append(lottoNo['drwNoDate'])      #추첨 날짜
        firstAccumamnt.append(lottoNo['firstAccumamnt'])    #1등 당첨액
        firstPrzwnerCo.append(lottoNo['firstPrzwnerCo'])    #1등 당첨된 사람 수
        firstWinamnt.append(lottoNo['firstWinamnt'])        #1등 당첨 금액

        lotto_dict = {"추첨일":drwNoDate, "Num1":drwtNo1, "Num2":drwtNo2, "Num3":drwtNo3, 
                      "Num4":drwtNo4, "Num5":drwtNo5, "Num6":drwtNo6, "bnsNum":bnusNo,
                      "총판매금액":totSellamnt, "총1등당첨금":firstAccumamnt, "1등당첨인원":firstPrzwnerCo, "1등수령액":firstWinamnt}
        cnt += 1
        i += 1

    df_lotto = pd.DataFrame(lotto_dict)

    return df_lotto, cnt

#추첨일, Num1, Num2, Num3, Num4, Num5, Num6, bnsNum, 총판매금액, 총1등당첨금, 1등당첨인원, 1등수령액
#lotto_df.to_csv("lotto_df_info.csv", index=False)
#lotto_df.sort_values(by=['1등수령액'], axis=0, ascending=False).head(10)    #1등수령액 열을 기준으로 내림차순 정렬후 10개만



if __name__=="__main__":
    while True:
        MinDrwNo = int(input("몇 회부터 분석하시겠습니까? "))
        if 0<MinDrwNo<MaxDrwNo:
            break

    lotto_df, count = getLottoWinInfo(MinDrwNo, count)
    all_nums = list(lotto_df['Num1'])+list(lotto_df['Num2'])+list(lotto_df['Num3'])+list(lotto_df['Num4'])+list(lotto_df['Num5'])+list(lotto_df['Num6'])
    all_nums_cnt_dic = Counter(all_nums)
    
    outputfile = "Lotto_Analysis.txt"
    with open(outputfile, "w") as fout:
        fwt = fout.write

        fwt("\n=========================Lotto Number 분석기==============================\n\n")
        fwt("총 "+str(MaxDrwNo-MinDrwNo)+ "회 차수 당첨 번호 분포:\n")

        #TOTAL = [drwtNo1, drwtNo2, drwtNo3, drwtNo4, drwtNo5, drwtNo6]
        TOTAL = [[] for i in range(len(drwtNo1))]
        for i in range(len(drwtNo1)):
            TOTAL[i].append(drwtNo1[i])
            TOTAL[i].append(drwtNo2[i])
            TOTAL[i].append(drwtNo3[i])
            TOTAL[i].append(drwtNo4[i])
            TOTAL[i].append(drwtNo5[i])
            TOTAL[i].append(drwtNo6[i])
            TOTAL[i].append(bnusNo[i])
            TOTAL[i].sort()

        for i in range(len(TOTAL)-1, 0, -1):
            n = 0
            for j in range(1, 46):
                if j != TOTAL[i][n]:
                    fwt("   ")
                else:       
                    fwt("{:<3d}".format(TOTAL[i][n]))
                    n += 1

                if n > 6:
                    n = 0
                if j%7==0 and j!=0:     
                    fwt("ㅣ")
            fwt("\n")

