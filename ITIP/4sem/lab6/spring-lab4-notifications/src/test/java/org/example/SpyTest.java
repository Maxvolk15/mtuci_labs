package org.example;

import java.util.ArrayList;
import java.util.List;

import org.junit.jupiter.api.Test;
import static org.mockito.Mockito.spy;
import static org.mockito.Mockito.verify;

class SpyTest {

    @Test
    void shouldVerifySpyListAdd() {
        List<String> list = new ArrayList<>();
        List<String> spyList = spy(list);

        spyList.add("Spring");

        verify(spyList).add("Spring");
    }
}
