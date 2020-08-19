using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class CameraMoveRotation : MonoBehaviour
{

    public GameObject player;
    private Vector3 offset;

    void LateUpdate()
    {
        transform.position = new Vector3(player.transform.position.x - 10 * Mathf.Sin(PlayerMoveRotation.rotation), 10+player.transform.position.y, player.transform.position.z - 10 * Mathf.Cos(PlayerMoveRotation.rotation));
        transform.LookAt(player.transform);
    }
}
