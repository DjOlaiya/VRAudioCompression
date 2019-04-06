using System.Collections;
using System.Collections.Generic;
using UnityEngine;

[RequireComponent(typeof(AudioSource))]
public class InitAudio : MonoBehaviour
{
    //all my declarations
     public const int numBands=32;
     public const int numSamples=4096;
     public AudioClip original;
        public AudioClip compressed;
    AudioSource  _audio;
    
    public static float[] _sample = new float[numSamples]; //once i make it static it wont show up in unity cos it cant be changed
    public static float[] _freqGroupd=new float[numBands];
    public static float[] _buffer = new float[numBands];
    void Start()
    {
        _audio = GetComponent<AudioSource>();
        _audio.PlayOneShot(original);
        _audio.PlayOneShot(compressed);
    }

  
    void Update()
    {
        GetAudioSpectrum();   
        GroupFreq();    
    }

//get audio and perform FFT
    void GetAudioSpectrum()
    {
        _audio.GetSpectrumData(_sample,0,FFTWindow.BlackmanHarris);    
    }

//take freq samples and group into bands for more spectral range
 void GroupFreq()
    {
        /*
        220050/1024= 5.38hz/sample_el
        split this into 1024 bands. If I do it evenly then 21.53hz/band. 
        If I try to do it using powers of 2 like he did, I end up with
        really small values in the range 0-1 for the first few values.

         */
        int sampleID =0;
        for(int i=0;i<numBands;i++)
        {
            int samplePerBand= 32;
            float avg=0;
            for(int j=0;j<samplePerBand;j++)
            {
                avg+= _sample[sampleID]; //*(sampleID+1);
                sampleID++;
            }
            avg/=samplePerBand;
        //valuesin arr are small so mult by 10 to make
            _freqGroupd[i]=avg*10;
        }

    }

    void thirdOctaveBands()
    {

    }


}


   