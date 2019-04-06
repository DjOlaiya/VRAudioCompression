using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class FreqCompress : MonoBehaviour
{
       const int buffsize=FreqBand.max_time;
    public Transform prefabC;
    public float _Mult,_startvalue;
    public static int N =InitAudio.numBands;
    //Transform[] _bandarray= new Transform[N];
    Transform [,] _bandarray2dC = new Transform[buffsize, N];
    public float[,] _ampArr2dC = new float[buffsize,N];
     int time=0; 
    
    void Start()
    {
       instantiateShapes();
    }


    void instantiateShapes()
    {
        float stepSize=2f/N;
        Vector3 scale= Vector3.one*stepSize;
        Vector3 position;
        position.y=0;
        time = 0;

        for(int i=0; i<N; i++){
            for(int j=0;j<N; j++){
                _ampArr2dC[i,j] = 1;
            }
        }

        for(int i = 0; i< N; i++){
            for(int j = 0; j<N; j++){
                Transform _spect = Instantiate(prefabC);
                position.x = j;
                position.z = i;
                _spect.localPosition = position;
                _spect.localScale = scale;
                _spect.SetParent(transform);
                _bandarray2dC[i,j] = _spect;

            }
        } 
    }
   void Update()
    {
        time +=1;
        buffupdate();
        BandAmpFn();
    }
  void BandAmpFn()
    {
            for(int i=time%buffsize; i>=0; i--)
            {
                for(int j=0; j<N; j++)
                {
                    _bandarray2dC[i,j].transform.localScale = new Vector3(transform.localScale.x,
                    (Mathf.Abs(_ampArr2dC[i,j]*_Mult))+_startvalue,transform.localScale.z);
                    
                }
            }

            for(int i= buffsize-1; i>time%buffsize; i--)
            {
                for(int j=0; j<N; j++)
                {
                    _bandarray2dC[i,j].transform.localScale = new Vector3(transform.localScale.x,
                    (_ampArr2dC[i,j]*_Mult)+_startvalue,transform.localScale.z);
                }
            }

    }

  void buffupdate()
    {
        for (int i = 0; i < N; i++) {
            _ampArr2dC[time%buffsize, i] = InitAudio._freqGroupd[i];

            if (time < buffsize) {
                Debug.Log(time + i + _ampArr2dC[time, i]);
            }
        }
        
    }


    // void BandAmpFn()
    //     {
        
    //         for(int i = 0; i<N;i++)
    //         {
    //             for(int j = 1; j<N; j++)
    //             {
    //                 _ampArr2dC[i,j] = _ampArr2dC[i,j-1];
    //             }
    //         }

    //         for(int x = 0; x<N; x++)
    //         {
    //             _ampArr2dC[x, 0] = InitAudio._freqGroupd[x];
    //             //time ++;
    //         }

    //         for(int i=0; i<N; i++)
    //         {
    //             for(int j=0; j<N; j++)
    //             {
    //                 _bandarray2dCC[i,j].transform.localScale = new Vector3(transform.localScale.x,
    //                 (_ampArr2dC[j,i]*_Mult)+_startvalue,transform.localScale.z);
    //             }
    //         }
    //     }
   
}
