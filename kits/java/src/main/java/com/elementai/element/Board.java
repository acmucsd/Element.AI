package com.elementai.element;

import com.fasterxml.jackson.annotation.JsonProperty;

// import java.util.Map;

public class Board {
    @JsonProperty("board_state")
    public int[][] boardState;

    @JsonProperty("players_state")
    public int[][] playersState;
}