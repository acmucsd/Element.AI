package com.elementai.element;

import com.fasterxml.jackson.annotation.JsonProperty;

import java.util.Map;

public class Obs {
    @JsonProperty("players")
    public Map<String, String> playerData;
    @JsonProperty("board")
    public Board board;
    @JsonProperty("real_env_steps")
    public int realEnvSteps;
}