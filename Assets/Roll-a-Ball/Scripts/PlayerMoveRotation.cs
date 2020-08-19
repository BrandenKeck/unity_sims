using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class PlayerMoveRotation : MonoBehaviour
{
    public static float rotation;

    private Rigidbody rb;
    private float moveVector;
    private float rotateVelocity;

    private void Start()
    {
        rb = GetComponent<Rigidbody>();
    }

    void FixedUpdate()
    {

        bool forward = Input.GetKey(KeyCode.UpArrow);
        bool backward = Input.GetKey(KeyCode.DownArrow);
        bool rotateLeft = Input.GetKey(KeyCode.LeftArrow);
        bool rotateRight = Input.GetKey(KeyCode.RightArrow);

        if (forward) { moveVector = 15; }
        else if (backward) { moveVector = -15; }
        else { moveVector = 0; }

        if (rotateLeft){ rotateVelocity = -0.04f; }
        else if (rotateRight){ rotateVelocity = 0.04f; }
        else{ rotateVelocity = 0; }

        rotation = rotation + rotateVelocity;
        rb.AddForce(new Vector3(moveVector*Mathf.Sin(rotation), 0.0f, moveVector * Mathf.Cos(rotation)));
    }
}
