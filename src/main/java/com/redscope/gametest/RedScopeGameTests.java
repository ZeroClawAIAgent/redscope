package com.redscope.gametest;

import net.minecraft.test.GameTest;
import net.minecraft.test.TestContext;
import net.minecraft.fabric.api.gametest.v1.FabricGameTest;

public class RedScopeGameTests implements FabricGameTest {
    @GameTest(templateName = "redscope:redstone_line_16")
    public void testSignalDeadEndDetection(TestContext context) {
        context.executeAfterDelay(() -> {
            // TODO: Run FaultDetector and assert faults contain "signal" and "missing receiver"
            context.complete();
        });
    }

    @GameTest(templateName = "redscope:piston_obsidian")
    public void testPistonUnmovableBlock(TestContext context) {
        context.addIndefiniteTask(() -> {
            // TODO: Run FaultDetector and assert "piston pushing unmovable block" fault
            context.complete();
        });
    }

    @GameTest(templateName = "redscope:comparator_wrong_mode")
    public void testComparatorWrongMode(TestContext context) {
        context.addIndefiniteTask(() -> {
            // TODO: Assert comparator fault
            context.complete();
        });
    }

    @GameTest(templateName = "redscope:torch_burnout")
    public void testTorchBurnout(TestContext context) {
        context.runAtTick(80, () -> {
            // TODO: Assert torch burnout fault detected
            context.complete();
        });
    }

    @GameTest(templateName = "redscope:repeater_wrong_direction")
    public void testRepeaterWrongDirection(TestContext context) {
        context.addIndefiniteTask(() -> {
            // TODO: Assert repeater direction fault
            context.complete();
        });
    }
}
