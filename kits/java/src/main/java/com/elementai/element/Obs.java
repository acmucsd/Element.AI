package com.elementai.element;

import com.fasterxml.jackson.annotation.JsonProperty;

import java.util.Map;

public class Obs {
    // @JsonProperty("player_0")
    // public Map<String, Player> playerData;
    @JsonProperty("board")
    public Board board;
}