package com.redscope.model;

import java.util.List;

public record SignalPath(List<RedstoneComponent> components, int totalDelay) {
}
