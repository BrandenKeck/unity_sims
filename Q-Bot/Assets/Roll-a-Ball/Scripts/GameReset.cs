using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using UnityEngine.SceneManagement;

public class GameReset : MonoBehaviour
{

    public float timeLimit = 90;
    public int winCount = 8;
    public Text timerText;
    public Text winsText;
    public Text lossesText;

    private float gameTimer;
    private float timeRemaining;
    private int count;
    private int wins;
    private int losses;

    [RuntimeInitializeOnLoadMethod(RuntimeInitializeLoadType.BeforeSceneLoad)]
    static void OnBeforeSceneLoadRuntimeMethod()
    {
        PlayerPrefs.SetInt("Wins", 0);
        PlayerPrefs.SetInt("Losses", 0);
    }

    private void Start()
    {
        if (!PlayerPrefs.HasKey("Wins") || !PlayerPrefs.HasKey("Losses"))
        {
            PlayerPrefs.SetInt("Wins", 0);
            PlayerPrefs.SetInt("Losses", 0);
        }

        gameTimer = 0;
        timeRemaining = timeLimit;
        wins = PlayerPrefs.GetInt("Wins");
        losses = PlayerPrefs.GetInt("Losses");

        setGameText();
    }

    private void Update()
    {
        gameTimer = gameTimer + Time.deltaTime;
        timeRemaining = timeLimit - gameTimer;
        count = PlayerCollision.publicCount;
        setGameText();

        if (count >= winCount)
        {
            PlayerPrefs.SetInt("Wins", wins + 1);
            SceneManager.LoadScene("main");
        }
        if (timeRemaining <= 0)
        {
            PlayerPrefs.SetInt("Losses", losses + 1);
            SceneManager.LoadScene("main");
        }

    }

    void setGameText()
    {
        timerText.text = "Time Remaining: " + Mathf.RoundToInt(timeRemaining).ToString() + " sec";
        winsText.text = "Number of Wins: " + wins.ToString();
        lossesText.text = "Number of Losses: " + losses.ToString();
    }
}
