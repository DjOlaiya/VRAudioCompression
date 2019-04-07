using System.Collections;
using System.Collections.Generic;
using UnityEngine;
public class FreqBand: MonoBehaviour
{
    public const int max_time = 16;
    public Transform prefab;
    public GameObject _SpectralBands;
    public float _Mult,_startvalue;
    public static int N =InitAudio.numBands;
    GameObject[] _mybands = new GameObject[N];
    Transform [,] _bandarray2d = new Transform[max_time, N];
    
    public float[,] time_Buff=new float[max_time, N];
    public float[,] _ampArr2d = new float[N,N];


    public int curr_time=0;
        
void Start()
{
    instantiateShapes();
}

//create 1D array of shapes based on freq bands
    void instantiateShapes()
    {
        float stepSize=2f/N;
        Vector3 scale= Vector3.one*stepSize;
        Vector3 position;
        position.y=0;
    
        for(int i=0; i<N; i++){
            for(int j=0;j<N; j++){
                _ampArr2d[i,j] = 1;
            }
        }

        for(int i = 0; i< N; i++){
            for(int j = 0; j<N; j++){
                Transform _spect = Instantiate(prefab);
                position.x = j;
                position.z = i;
                _spect.localPosition = position;
                _spect.localScale = scale;
                _spect.SetParent(transform);
                _bandarray2d[i,j] = _spect;
            }
        }
    }
  
    void Update()
    {
        curr_time+=1;
        buffupdate();
        BandAmpFn();
    }

    void buffupdate()
    {
        for (int i = 0; i < N; i++) {
            time_Buff[curr_time%max_time, i] = InitAudio._freqGroupd[i];

            if (curr_time < max_time) {
                Debug.Log(curr_time + i + time_Buff[curr_time, i]);
            }
        }    
    }
    
//creates the dynamic change in the shapes along y axis
    void BandAmpFn()
    {
            for(int i=curr_time%max_time; i>=0; i--)
            {
                for(int j=0; j<N; j++)
                {
                    _bandarray2d[i,j].transform.localScale = new Vector3(transform.localScale.x,
                    (Mathf.Abs(time_Buff[i,j]*_Mult))+_startvalue,transform.localScale.z);   
                }
            }

            for(int i= max_time-1; i>curr_time%max_time; i--)
            {
                for(int j=0; j<N; j++)
                {
                    _bandarray2d[i,j].transform.localScale = new Vector3(transform.localScale.x,
                    (time_Buff[i,j]*_Mult)+_startvalue,transform.localScale.z);
                }
            }

    }
    
}









// List<float[]> dB_buffList = new List<float[]>();
// while(time < 16)
// {
//     float[] dbBuff = new float[10];
//     dbBuff[0] = "whatever";
//     myArrayList.Add(blah);

    //  public unsafe void updateBuff(int[] graphBuff,float* curr_freq, int max_time)
    //     {
    //        fixed(int* dBvalues=index)
    //        {
    //            for (int i = 1; i < max_time) {
    //                graphBuff[i] = graphBuff[i - 1];
    //            }

    //            graphBuff[0] = curr_freq;
    //        }
    //     }

