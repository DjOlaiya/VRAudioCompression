using System.Collections;
using System.Collections.Generic;
using UnityEngine;

[RequireComponent(typeof(AudioSource))]
public class InitAudio : MonoBehaviour
{
    //all my declarations
     public const int numBands=32;
     public const int numSamples=1024;
    AudioSource  _audio;
    
    public static float[] _sample = new float[numSamples]; //once i make it static it wont show up in unity cos it cant be changed
    public static float[] _freqGroupd=new float[numBands];
    public static float[] _buffer = new float[numBands];
    void Start()
    {
        _audio=GetComponent<AudioSource>();
        _audio.clip=Resources.Load<AudioClip>("faded");
        _audio.Play();
    }

  
    void Update()
    {
        GetAudioSpectrum();   
        thirdOctaveBands();   
    }

//get audio and perform FFT
    void GetAudioSpectrum()
    {
        _audio.GetSpectrumData(_sample,0,FFTWindow.BlackmanHarris);  
        _audio.GetSpectrumData(_buffer,0,FFTWindow.BlackmanHarris);
        // return _aud;   
    }

// split samples up using third octave calculations
    void thirdOctaveBands()
    {
        int count=0;
         float ctr=16;
        for(int j=0;j<numBands;j++)
        {
            float avg=0;
            ctr=ctr*Mathf.Pow(2,1/3);
            _buffer[j]=ctr;
            int ctrindex=Mathf.RoundToInt(ctr);
            for(int l=0;l<ctrindex;l++){
                avg+=_sample[count]*(count+1);
                count++;
            }
            avg/=ctrindex;
            _freqGroupd[j]=avg;
        }
    }
}


   