using System.Collections;
using System.Collections.Generic;
using UnityEngine;
public class FreqBand: MonoBehaviour
{
    public Transform prefab;
     public GameObject _SpectralBands;
    public float _Mult,_startvalue;
    public static int N =InitAudio.numBands;
    GameObject[] _mybands = new GameObject[N];
    Transform[] _bandarray= new Transform[N];
     public  float[] _prevfreqband = new float[N];
    
    float[] _CurFreqBand = new float[N];
    
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
        position.z=0;

         for(int i =0,z=0;i<N;z++)
            {
                for(int x=0;x<N;x++,i++)
                {
                 Transform _spect=Instantiate(prefab);
                    position.x=i;
                    _spect.localPosition=position;
                    _spect.localScale=scale;
                    _spect.name="shape"+i;
                    _spect.SetParent(transform);
                    _bandarray[i]= _spect;
                }    
            }
        //  for(int i=0; i<N; i++)
        // {
        //     GameObject _SpectralBand1024 = (GameObject)Instantiate(_SpectralBands);
        //     _SpectralBand1024.transform.position = this.transform.position;
        //     _SpectralBand1024.transform.parent=this.transform;
        //     _SpectralBand1024.name="spectralBandwidth" + i;
        //     _SpectralBand1024.transform.position=new Vector3(i,i,10);
        //     _mybands[i] = _SpectralBand1024;
        // }
    }
  
    void Update()
    {
        BandAmpFn();
    }

//creates the dynamic change in the shapes along y axis
    void BandAmpFn()
    {
        for(int i=0;i<N;i++)
        {
                _bandarray[i].transform.localScale = new Vector3(transform.localScale.x,
                (InitAudio._freqGroupd[i]*_Mult)+_startvalue,transform.localScale.z);
        }
        
        // for(int i=0;i<N;i++)
        // {
        //         _mybands[i].transform.localScale = new Vector3(transform.localScale.x,
        //         (InitAudio._freqGroupd[i]*_Mult)+_startvalue,transform.localScale.z);
        // }
    }
   
    //take and store old sample values to use graph.  
    public void setZdimension(float[] spectra)
    {
        for(int i=0;i<8;i++)
        {
            _CurFreqBand.CopyTo(_prevfreqband,0);
            spectra.CopyTo(_CurFreqBand,0);              
        }
    }

//  public void arrinst()
//     {
//         for(int i=0 ;i<8 ;i++)
//         {
//             public  float[] _prevfreqband = new float[N]; 
//             _prevfreqband.name="_prefreqband"+i;  
//         }
//     }
}
