using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class DroneMove : MonoBehaviour
{

    public float speedFactor = 10;
    public float liftVelocityCap = 10;
    public float moveVelocityCap = 10;
    public float rotateVelocityCap = 10;
    public float pitchVelocityCap = 10;
    public float rollVelocityCap = 10;

    private Rigidbody rb;
    private float liftVelocity;
    private float moveVelocity;
    private float rotateVelocity;
    private float pitchVelocity;
    private float rollVelocity;

    private void Start()
    {
        rb = GetComponent<Rigidbody>();
        liftVelocity = 0;
        moveVelocity = 0;
        rotateVelocity = 0;
        pitchVelocity = 0;
        rollVelocity = 0;
    }

    void FixedUpdate()
    {
        bool up = Input.GetKey(KeyCode.Q);
        bool down = Input.GetKey(KeyCode.E);
        bool forward = Input.GetKey(KeyCode.W);
        bool backward = Input.GetKey(KeyCode.S);
        bool rotateLeft = Input.GetKey(KeyCode.A);
        bool rotateRight = Input.GetKey(KeyCode.D);
        bool pitchForward = Input.GetKey(KeyCode.UpArrow);
        bool pitchBackward = Input.GetKey(KeyCode.DownArrow);
        bool rollLeft = Input.GetKey(KeyCode.LeftArrow);
        bool rollRight = Input.GetKey(KeyCode.RightArrow);

        if (up)
        {
            liftVelocity = liftVelocity + speedFactor;
            if (liftVelocity > liftVelocityCap)
            {
                liftVelocity = liftVelocityCap;
            }
        }else if (down)
        {
            liftVelocity = liftVelocity - speedFactor;
            if (liftVelocity < -1*liftVelocityCap)
            {
                liftVelocity = -1*liftVelocityCap;
            }
        }
        else
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

        if (pitchBackward)
        {
            pitchVelocity = pitchVelocity - 100 * speedFactor;
            if (pitchVelocity < -1 * pitchVelocityCap)
            {
                pitchVelocity = -1 * pitchVelocityCap;
            }
        }
        else if (pitchForward)
        {
            pitchVelocity = pitchVelocity + 100 * speedFactor;
            if (pitchVelocity > pitchVelocityCap)
            {
                pitchVelocity = pitchVelocityCap;
            }
        }
        else
        {
            pitchVelocity = 0;
        }

        if (rollRight)
        {
            rollVelocity = rollVelocity - 100 * speedFactor;
            if (rollVelocity < -1 * rollVelocityCap)
            {
                rollVelocity = -1 * rollVelocityCap;
            }
        }
        else if (rollLeft)
        {
            rollVelocity = rollVelocity + 100 * speedFactor;
            if (rollVelocity > rollVelocityCap)
            {
                rollVelocity = rollVelocityCap;
            }
        }
        else
        {
            rollVelocity = 0;
        }

        transform.Translate(new Vector3(moveVelocity, liftVelocity, 0) * Time.deltaTime);
        transform.Rotate(new Vector3(rollVelocity, rotateVelocity, pitchVelocity) * Time.deltaTime);

        if(!up && !down && !forward && !backward)
        {
            rb.velocity = Vector3.zero;
        }
        if (!rotateLeft && !rotateRight && !pitchForward && !pitchBackward && !rollLeft && !rollRight)
        {
            rb.angularVelocity = Vector3.zero;
        }

    }
}
