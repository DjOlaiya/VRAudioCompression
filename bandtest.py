

# for(int i=0;i<8;i++)
#     //      {
#     //             float average=0;
#     //             //or just do it as i+1
#     //             int sampleCount = (int)Mathf.Pow(2,i)*2;
#     //             //here we are generating all 512 samples
#     //             if(i==7)
#     //             {
#     //                 sampleCount+=2; //why?
#     //             }
#     //         for (int j=0;j<sampleCount;j++)
#     //         {
#     //             average += _samples[count]* (count+1);
#     //             count++;
#     //         }   
#     //         average/=count;
#     //         freqband[i] = average*10
init=1000
arr=[]
# for i in range(1,33):
#     init= pow(2,[-18:13]/3)
#     print('value:',1000+init)
#     print(init)

y=-18
arr=[]
q=1000

for i in range(0,19):
    q=q/pow(2,1/3)
    print(q)
print("Now we are done with low bands")
c=16
for i in range(0,19):
    c=c*pow(2,1/3)
    print(c)



