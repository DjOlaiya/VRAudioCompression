using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Create_N_spectral_Obj : MonoBehaviour
{
    public GameObject _SpectralObjects;
    public float _ScalarMult;
    public static int n =InitAudio.numSamples;
    GameObject[] _sampleobj = new GameObject[n];

    void Start()
    {
        CreateSampleShapes();
    }
    
    //init all 1024  shapes.
    void CreateSampleShapes()
    {
        for(int i=0; i<n; i++)
        {
            GameObject _spectralobjInstance = (GameObject)Instantiate(_SpectralObjects);
            _spectralobjInstance.transform.position = this.transform.position;
            _spectralobjInstance.transform.parent=this.transform;
            _spectralobjInstance.name="spectral obj" + i;
            _spectralobjInstance.transform.position=new Vector3(i,i,0);
            _sampleobj[i] = _spectralobjInstance;
        }
    }
    void Update()
    {
        amplitudeFn();
    }

//change in y axis of shapes
    void amplitudeFn()
    {
        for(int i=0;i<n;i++)
        {
            if(_sampleobj !=null)
            {
                _sampleobj[i].transform.localScale = new Vector3(1,(InitAudio._sample[i]*_ScalarMult)+1,1);
            }
        }
    }
}
