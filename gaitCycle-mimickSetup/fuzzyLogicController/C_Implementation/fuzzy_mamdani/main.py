import time
import math

DIMENSION_max = 200
LINGUISTIC_max = 200 # Max swarm size
PI =  3.1415927
g_fcm = 1.25
eta = 0.01

#file management to be takn care of
li = [4,5]
lo = [5]
i_inp = [1.04, 30]
linguisticinput = [[-2,-1,1,2],[-2,-1,0,1,2]]
linguisticoutput = [-2,-1,0,1,2]
linguisticoutput_if_else = [[0],[1],[-1],[-1],[0],[0],[0],[2],[0],[0],[0],[0],[1],[0],[0],[0],[0],[0],[0],[0]]
linguistic_range_input_min = [[0.1,0.1,0.8,1.5],[-90,-90,-45,0,45]]
linguistic_range_input_max = [[0.8,1.5,2.2,2.2],[-45,0,45,90,90]]
linguistic_range_output_min = [-90,-90,-45,0,-45]
linguistic_range_output_max = [-45,0,45,90,90]

def centroid_under_curve(index_output_linguistic,i_lterni,centroid,y_upper,start,end,lo,no_output,i_inp,linguistic_range_input_min,linguistic_range_input_max,linguistic_range_output_min,linguistic_range_output_max):
    i_lter = 0
    dimension = 0
    ii_index=0
    for dimension in range(no_output):
        for ii_index in range(i_lterni):
            if index_output_linguistic[dimension][ii_index] == 0:
                start[dimension][ii_index]=linguistic_range_output_min[dimension][index_output_linguistic[dimension][ii_index]]
                end[dimension][ii_index]=linguistic_range_output_min[dimension][index_output_linguistic[dimension][ii_index]]+(-linguistic_range_output_min[dimension][index_output_linguistic[dimension][ii_index]]+linguistic_range_output_max[dimension][index_output_linguistic[dimension][ii_index]])*(1-y_upper[dimension][ii_index])
                centroid[dimension][ii_index]=(start[dimension][ii_index]+end[dimension][ii_index]+linguistic_range_output_min[dimension][index_output_linguistic[dimension][ii_index]]+linguistic_range_output_max[dimension][index_output_linguistic[dimension][ii_index]])/4
            elif index_output_linguistic[dimension][ii_index]==lo[dimension]-1:
                start[dimension][ii_index]=linguistic_range_output_max[dimension][index_output_linguistic[dimension][ii_index]]-(linguistic_range_output_max[dimension][index_output_linguistic[dimension][ii_index]]-linguistic_range_output_min[dimension][index_output_linguistic[dimension][ii_index]])*(1-y_upper[dimension][ii_index])
                end[dimension][ii_index]=linguistic_range_output_max[dimension][index_output_linguistic[dimension][ii_index]]
                centroid[dimension][ii_index]=0.25*(start[dimension][ii_index]+end[dimension][ii_index]+linguistic_range_output_min[dimension][index_output_linguistic[dimension][ii_index]]+linguistic_range_output_max[dimension][index_output_linguistic[dimension][ii_index]])
            else:
                start[dimension][ii_index]=0.5*(linguistic_range_output_min[dimension][index_output_linguistic[dimension][ii_index]]+linguistic_range_output_max[dimension][index_output_linguistic[dimension][ii_index]])-0.5*(-linguistic_range_output_min[dimension][index_output_linguistic[dimension][ii_index]]+linguistic_range_output_max[dimension][index_output_linguistic[dimension][ii_index]])*(1-y_upper[dimension][ii_index])
                end[dimension][ii_index]=0.5*(linguistic_range_output_min[dimension][index_output_linguistic[dimension][ii_index]]+linguistic_range_output_max[dimension][index_output_linguistic[dimension][ii_index]])+0.5*(-linguistic_range_output_min[dimension][index_output_linguistic[dimension][ii_index]]+linguistic_range_output_max[dimension][index_output_linguistic[dimension][ii_index]])*(1-y_upper[dimension][ii_index])
                centroid[dimension][ii_index]=0.25*(start[dimension][ii_index]+end[dimension][ii_index]+linguistic_range_output_max[dimension][index_output_linguistic[dimension][ii_index]]+linguistic_range_output_min[dimension][index_output_linguistic[dimension][ii_index]])

def area_under_curve(index_output_linguistic,i_lterni,area,y_upper,start,end,lo,no_output,i_inp,linguistic_range_input_min,linguistic_range_input_max,linguistic_range_output_min,linguistic_range_output_max):
    i_lter=0
    dimension=0
    ii_index=0;
    for dimension in range(no_output):
        for ii_index in range(i_lterni):
            if index_output_linguistic[dimension][ii_index]==0:
                start[dimension][ii_index]=linguistic_range_output_min[dimension][index_output_linguistic[dimension][ii_index]]
                end[dimension][ii_index]=linguistic_range_output_max[dimension][index_output_linguistic[dimension][ii_index]]
                area[dimension][ii_index]=fabs((1/(start[dimension][ii_index]-end[dimension][ii_index]))*(0.5*(end[dimension][0]*end[dimension][ii_index]-start[dimension][ii_index]*start[dimension][ii_index])-end[dimension][ii_index]*(end[dimension][ii_index]-start[dimension][ii_index])))
                area[dimension][ii_index]=(area[dimension][ii_index]-(1-y_upper[dimension][ii_index])*(1-y_upper[dimension][ii_index])*area[dimension][ii_index])
            elif index_output_linguistic[dimension][ii_index]==lo[dimension]-1:
                start[dimension][ii_index]=linguistic_range_output_min[dimension][index_output_linguistic[dimension][ii_index]]
                end[dimension][ii_index]=linguistic_range_output_max[dimension][index_output_linguistic[dimension][ii_index]]
                area[dimension][ii_index]=fabs((1/(start[dimension][ii_index]-end[dimension][ii_index]))*(0.5*(end[dimension][ii_index]*end[dimension][ii_index]-start[dimension][ii_index]*start[dimension][ii_index])-end[dimension][ii_index]*(end[dimension][ii_index]-start[dimension][ii_index])))
                area[dimension][ii_index]=(area[dimension][ii_index]-(1-y_upper[dimension][ii_index])*(1-y_upper[dimension][ii_index])*area[dimension][ii_index])
            else:
                start[dimension][ii_index]=0.5*(linguistic_range_output_min[dimension][index_output_linguistic[dimension][ii_index]]+linguistic_range_output_max[dimension][index_output_linguistic[dimension][ii_index]])
                end[dimension][ii_index]=linguistic_range_output_max[dimension][index_output_linguistic[dimension][ii_index]]
                area[dimension][ii_index]=fabs((1/(start[dimension][ii_index]-end[dimension][ii_index]))*(0.5*(end[dimension][ii_index]*end[dimension][ii_index]-start[dimension][ii_index]*start[dimension][ii_index])-end[dimension][ii_index]*(end[dimension][ii_index]-start[dimension][ii_index])))
                area[dimension][ii_index]=2*(area[dimension][ii_index]-(1-y_upper[dimension][ii_index])*(1-y_upper[dimension][ii_index])*area[dimension][ii_index])

def membership_function(membership_function_value,ii,linguistic_number,li,no_input,i_inp,linguistic_range_input_min,linguistic_range_input_max,linguistic_range_output_min,linguistic_range_output_max):
    i_lter=0
    dimension=0
    for dimension in range(no_input):
        membership_function_value[dimension][0]=1-((i_inp[dimension]-linguistic_range_input_min[dimension][0])/(linguistic_range_input_max[dimension][0]-linguistic_range_input_min[dimension][0]));
        for i_lter in range(li[dimension]-1):
            membership_function_value[dimension][i_lter]=max(min(((i_inp[dimension]-linguistic_range_input_min[dimension][i_lter])/((0.5*(linguistic_range_input_max[dimension][i_lter]+linguistic_range_input_min[dimension][i_lter]))-linguistic_range_input_min[dimension][i_lter])),((linguistic_range_input_max[dimension][i_lter]-i_inp[dimension])/(linguistic_range_input_max[dimension][i_lter]-(0.5*(linguistic_range_input_max[dimension][i_lter]+linguistic_range_input_min[dimension][i_lter]))))),0);
    membership_function_value[dimension][li[dimension]-1]=1-((linguistic_range_input_max[dimension][li[dimension]-1]-i_inp[dimension])/(linguistic_range_input_max[dimension][li[dimension]-1]-linguistic_range_input_min[dimension][li[dimension]-1]));

def data_base(ii,linguistic_number,li,no_input,i_inp,linguistic_range_input_min,linguistic_range_input_max, linguistic_range_output_min,linguistic_range_output_max):
    i_lter = 0
    dimension = 0
    for dimension in range(no_input):
        ii[dimension]=0;
        for i_lter in range(li[dimension]):
            if ((i_inp[dimension]>=linguistic_range_input_min[dimension][i_lter]) & (i_inp[dimension]<=linguistic_range_input_max[dimension][i_lter])):
                linguistic_number[dimension][ii[dimension]]=i_lter;
                ii[dimension]=ii[dimension]+1;


def rule_base(i_ltern,in_indext,li,lo,linguisticinput1,linguisticinput,linguisticoutput1,linguisticoutput_if_else,ii,ln, i_lternt,linguisticoutput,index_output_linguistic,no_output):
    i_lter=0
    i_lter1=0
    i_lter2=0
    i_lter3=0
    dimension=0
    ii_index=0
    i_ltern=0;
    for i_lter2 in range(ii[0]):
        for i_lter3 in range(ii[1]):
            i_lternt = 0
            for i_lter in range(li[0]):
                for i_lter1 in range(li[1]):
                    in_indext=i_lternt
                    i_lternt=i_lternt+1
                    if ((linguisticinput1[0][ln[0][i_lter2]]==linguisticinput[0][i_lter])&(linguisticinput1[1][ln[1][i_lter3]]==linguisticinput[1][i_lter1])):
                        linguisticoutput1[0][i_ltern]=linguisticoutput_if_else[0][in_indext]
                        i_ltern = i_ltern+1
    for dimension in range(no_output):
        for ii_index in range(i_ltern):
            for i_lter in range(lo[0]):
                if (linguisticoutput1[0][ii_index]==linguisticoutput[0][i_lter]):
                    index_output_linguistic[0][ii_index]=i_lter

def main():
    no_output = 1
    no_input = 2
    for dimension in range(no_input):
        for i_lter in range(li[dimension]):
            print(linguistic_range_input_min[dimension][i_lter]),
            print(linguistic_range_input_max[dimension][i_lter])
        print("\n")
    print("\n")

    #Definitions
    inti_ltern =0
    i_lterni=0
    i_lter2=0
    i_lternt =0 
    i_lter3=0
    in_indext = 0
    min_input = [1.0]*200
    max_input = [1.0]*200
    min_output = [1.0]*200
    max_output= [1.0]*200
    sum_LCM= [1.0]*200
    sum_HCF= [1.0]*200
    LCM= [1.0]*200
    HCF= [1.0]*200
    crisp_output= [1.0]*200
    ii= [1.0]*200
    jj= [1.0]*200
    i_inp= [1.0]*200
    o_oup= [1.0]*200

    linguistic_number = [[0]*20]*20
    index_output_linguistic =  [[0]*20]*20
    membership_function_value_input= [[1.000] * 20]*20
    linguisticinput1= [[1.000 ]* 20]*20
    linguisticoutput1= [[1.000 ]* 20]*20
    linguisticoutput_if_else= [[1.000 ]* 20]*20
    area= [[1.000 ]* 20]*20
    centroid= [[1.000 ]* 20]*20
    y_upper= [[1.000 ]* 20]*20
    start= [[1.000 ]* 20]*20
    end= [[1.000 ]* 20]*20
    alpha= [[1.000 ]* 20]*20






    #for dimension in range(no_output):
    #    for i_lter in range(lo[dimension]):
    #        print(linguistic_range_output_min[dimension][i_lter])
    #        print("   ")
    #        print(linguistic_range_output_max[dimension][i_lter]))
    data_base(ii,linguistic_number,li,no_input,i_inp,linguistic_range_input_min,linguistic_range_input_max,linguistic_range_output_min,linguistic_range_output_max)
    for dimension in range(no_input):
        for iii in range(ii[dimension]):
            print(linguisticinput[dimension][linguistic_number[dimension][iii]])
    for dimension in range(no_input):
        for iii in range(ii[dimension]):
            linguisticinput1[dimension][linguistic_number[dimension][iii]]=linguisticinput[dimension][linguistic_number[dimension][iii]]
    rule_base(i_lterni,in_indext,li,lo,linguisticinput1,linguisticinput,linguisticoutput1,linguisticoutput_if_else,ii,linguistic_number,i_lternt,linguisticoutput,index_output_linguistic,no_output)
    print(i_lterni)
    print(linguisticoutput1[0])

    membership_function(membership_function_value_input,ii,linguistic_number,li,no_input,i_inp,linguistic_range_input_min,linguistic_range_input_max,linguistic_range_output_min,linguistic_range_output_max)
    for dimension in range(no_input):
        for iii in range(ii[dimension]):
            print(membership_function_value_input[dimension][linguistic_number[dimension][iii]])
    iii_index = 0;
    for dimension in range(no_input):
        for iii in range(ii[dimension]):
            for dimension1 in range(no_input):
                alpha[0][iii_index]=min(membership_function_value_input[dimension][linguistic_number[dimension][iii]],membership_function_value_input[dimension1][linguistic_number[dimension1][jjj]])
                print(alpha[0][iii_index])
                iii_index=iii_index+1
    area_under_curve(index_output_linguistic,i_lterni,area,alpha,start,end,lo,no_output,i_inp,linguistic_range_input_min,linguistic_range_input_max,linguistic_range_output_min,linguistic_range_output_max)
    #printf("\n");

    for dimension in range(no_output):
        for iii in range(i_lterni):
            print(area[dimension][iii])
    centroid_under_curve(index_output_linguistic,i_lterni,centroid,alpha,start,end,lo,no_output,i_inp,linguistic_range_input_min,linguistic_range_input_max,linguistic_range_output_min,linguistic_range_output_max)
    for dimension in range(no_output):
        for iii in range(i_lterni):
            print(centroid[dimension][iii])
    for dimension in range(no_output):
        LCM[dimension]=0
        HCF[dimension]=0
        for iii in range(i_lterni):
            LCM[dimension]=LCM[dimension]+area[dimension][iii]*centroid[dimension][iii]
            HCF[dimension]=HCF[dimension]+area[dimension][iii]
            crisp_output[dimension]=LCM[dimension]/HCF[dimension]
        print(crisp_output[dimension])

main()
