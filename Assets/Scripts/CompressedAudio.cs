using System.Collections;
using System.Collections.Generic;
using UnityEngine;

[RequireComponent(typeof(AudioSource))]
public class CompressedAudio : MonoBehaviour
{
    
    public static float[] _freqGroupC=new float[InitAudio.numBands];
    public static float[] _sampleC = new float[InitAudio.numSamples]; //once i make it static it wont show up in unity cos it cant be changed
 
    AudioSource _compressedAudio;
    // Start is called before the first frame update
    void Start()
    {
        _compressedAudio=GetComponent<AudioSource>();
    }

    // Update is called once per frame
    void Update()
    {
        GetAudioSpectrum();   
        GroupFreq();
    }


      void GetAudioSpectrum()
    {
        _compressedAudio.GetSpectrumData(_sampleC,0,FFTWindow.BlackmanHarris);
        
    }

    void GroupFreq()
    {
        int sampleID =0;
        for(int i=0;i<InitAudio.numBands;i++)
        {
            int samplePerBand= 32;
            float avg=0;
            for(int j=0;j<samplePerBand;j++)
            {
                avg+= _sampleC[sampleID]; //*(sampleID+1);
                sampleID++;
            }
            avg/=samplePerBand;
        //valuesin arr are small so mult by 10 to make
            _freqGroupC[i]=avg*10;
        }

    }
}
 

   