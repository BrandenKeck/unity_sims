using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class DroneMove : MonoBehaviour
{

    public float speedFactor = 10;
    public float liftVelocityCap = 10;
    public float moveVelocityCap = 10;
    public float rotateVelocityCap = 10;

    private Rigidbody rb;
    private float liftVelocity;
    private float moveVelocity;
    private float rotateVelocity;

    private void Start()
    {
        rb = GetComponent<Rigidbody>();
        liftVelocity = 0;
        moveVelocity = 0;
        rotateVelocity = 0;
    }

    void FixedUpdate()
    {
        bool lift = Input.GetKey(KeyCode.Space);
        bool forward = Input.GetKey(KeyCode.UpArrow);
        bool backward = Input.GetKey(KeyCode.DownArrow);
        bool rotateLeft = Input.GetKey(KeyCode.LeftArrow);
        bool rotateRight = Input.GetKey(KeyCode.RightArrow);

        if (lift)
        {
            liftVelocity = liftVelocity + speedFactor;
            if (liftVelocity > liftVelocityCap)
            {
                liftVelocity = liftVelocityCap;
            }
        }else
        {
            liftVelocity = 0;
        }

        if (forward)
        {
            moveVelocity = moveVelocity + speedFactor;
            if (moveVelocity > moveVelocityCap)
            {
                moveVelocity = moveVelocityCap;
            }
        }else if (backward)
        {
            moveVelocity = moveVelocity - speedFactor;
            if (moveVelocity < -1 * moveVelocityCap)
            {
                moveVelocity = -1 * moveVelocityCap;
            }
        }else
        {
            moveVelocity = 0;
        }

        if (rotateLeft)
        {
            rotateVelocity = rotateVelocity - 100 * speedFactor;
            if (rotateVelocity < -1 * rotateVelocityCap)
            {
                rotateVelocity = -1 * rotateVelocityCap;
            }
        }else if (rotateRight)
        {
            rotateVelocity = rotateVelocity + 100 * speedFactor;
            if (rotateVelocity > rotateVelocityCap)
            {
                rotateVelocity = rotateVelocityCap;
            }
        }else
        {
            rotateVelocity = 0;
        }

        transform.Translate(new Vector3(moveVelocity, liftVelocity, 0) * Time.deltaTime);
        transform.Rotate(new Vector3(0, rotateVelocity, 0) * Time.deltaTime);

    }
}
