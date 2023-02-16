package com.elementai.element;

import com.fasterxml.jackson.annotation.JsonProperty;

import java.util.Map;

public class Board {
    @JsonProperty
    public int[][] boardState;

    @JsonProperty
    public int[][] playersState;
}