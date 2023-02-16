package com.elementai.element;
import com.fasterxml.jackson.annotation.JsonProperty;

public class Player {
    @JsonProperty("player_num")
    public int playerNum;

    @JsonProperty("direction")
    public int[] direction;

    @JsonProperty("resetting")
    public boolean resetting;

    @JsonProperty("head")
    public int[] head;
    
    @JsonProperty("energy")
    public int energy;
    
    @JsonProperty("speed")
    public int speed;
}
