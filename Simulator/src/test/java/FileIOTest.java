import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

import javax.swing.*;
import java.awt.*;
import java.awt.geom.Line2D;
import java.io.File;
import java.io.IOException;
import java.net.URISyntaxException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.ArrayList;

import static org.junit.jupiter.api.Assertions.assertEquals;

public class FileIOTest
{
    private ArrayList<Block> blocks;
    private ArrayList<Block> wires;
    private JTextArea functionArea;
    private File outputFile;
    private DrawCircuit dummyPanel;

    @BeforeEach
    @SuppressWarnings("unchecked")
    void setup() throws IOException
    {
        Block.reset();
        blocks = new ArrayList<>();
        wires = new ArrayList<>();
        functionArea = new JTextArea();
        DrawingApp app = new DrawingApp();
        dummyPanel = app.getManager().getDrawCircuit();

        outputFile = new File("test_simulation.py");
        if (outputFile.exists()) outputFile.delete();

        functionArea.setText("def n(a):\n" + "    return (~a & 0b1)\n\n" +

                "def nsl(ps, i):\n" + "    a = (ps >> 1) & 1\n" + "    b = (ps >> 0) & 1\n" + "    d = (n(a) & b & n(i)) | (a & n(b) & n(i))\n" + "    e = (n(b) & n(i))\n" + "    return d << 1 | e\n\n" +

                "def ol(ps):\n" + "    return ps\n");

        // ----------- Create Blocks -----------

        Input pwmInput = new Input("PWM Input", new Rectangle(10, 10, 50, 50), Color.BLUE, dummyPanel);
        pwmInput.getMap().get("filePath");
        ((JTextField) pwmInput.getMap().get("filePath")).setText("Tests\\PWM.csv");

        Clock clk = new Clock("clk", new Rectangle(10, 70, 50, 50), Color.RED, dummyPanel);
        ((JTextField) clk.getMap().get("timePeriod")).setText("1");
        ((JTextField) clk.getMap().get("onTime")).setText("0.5");

        Moore mod4 = new Moore("Mod 4 Counter", new Rectangle(10, 130, 50, 50), Color.GREEN, dummyPanel);
        ((JSpinner) mod4.getMap().get("maxOutSize")).setValue(2);
        ((JSpinner) mod4.getMap().get("startingState")).setValue(0);
        ((JComboBox<String>) mod4.getMap().get("plot")).setSelectedIndex(0);
        ((JTextField) mod4.getMap().get("nsl")).setText("nsl");
        ((JTextField) mod4.getMap().get("ol")).setText("ol");

        Combinational syncReset = new Combinational("Sync Reset Comparator", new Rectangle(10, 190, 50, 50), Color.ORANGE, dummyPanel);
        ((JTextField) syncReset.getMap().get("func")).setText("lambda x: int((x & 3) == (x >> 2))");

        Combinational outputComp = new Combinational("Output Comparator", new Rectangle(10, 250, 50, 50), Color.YELLOW, dummyPanel);
        ((JTextField) outputComp.getMap().get("func")).setText("lambda x: int((x & 3) > (x >> 2))");

        Output finalOut = new Output("PWM Output", new Rectangle(10, 310, 50, 50), Color.MAGENTA, dummyPanel);
        ((JComboBox<String>) finalOut.getMap().get("plot")).setSelectedIndex(0);

        blocks.add(pwmInput);
        blocks.add(clk);
        blocks.add(mod4);
        blocks.add(syncReset);
        blocks.add(outputComp);
        blocks.add(finalOut);

        // ----------- Create Wires -----------

        Wire inputToComp = connect(pwmInput, outputComp);
        ((JTextField) (inputToComp.getMap().get("Output LSB (inclusive)"))).setText("0");
        ((JTextField) (inputToComp.getMap().get("Output MSB (exclusive)"))).setText("2");

        Wire inputToReset = connect(pwmInput, syncReset);
        ((JTextField) (inputToReset.getMap().get("Output LSB (inclusive)"))).setText("2");
        ((JTextField) (inputToReset.getMap().get("Output MSB (exclusive)"))).setText("4");

        wires.add(inputToComp);
        wires.add(connect(mod4, outputComp));
        wires.add(inputToReset);
        wires.add(connect(mod4, syncReset));
        wires.add(connect(syncReset, mod4));
        wires.add(connect(outputComp, finalOut));

        Wire clockWire = connect(clk, mod4);
        ((JComboBox<?>) clockWire.getMap().get("Is Clock Line")).setSelectedItem("True");
        wires.add(clockWire);
    }

    private Wire connect(Block a, Block b)
    {
        Wire w = new Wire("wire", new Line2D.Double(0, 0, 10, 10), Color.BLACK, dummyPanel);
        w.setBlock(a);
        w.setBlock(b);
        return w;
    }

    @Test
    void testPWMFileGeneration() throws IOException, URISyntaxException
    {
        // Act: Generate the output file
        FileIO.generateCircuitFile(outputFile.getAbsolutePath(), blocks, wires, functionArea, 0, 40);

        // Load actual output
        String actual = new String(Files.readAllBytes(outputFile.toPath()), java.nio.charset.StandardCharsets.UTF_8).replace("\r\n", "\n").trim();

        // Load expected file from src/test/resources/testFiles/
        Path expectedPath = Paths.get(ClassLoader.getSystemResource("testFiles/expectedOutput.py").toURI());

        String expected = new String(Files.readAllBytes(expectedPath), java.nio.charset.StandardCharsets.UTF_8).replace("\r\n", "\n").trim();

        // Assert comparison
        assertEquals(expected, actual, "Generated PWM file does not match expected output.");
    }

    @AfterEach
    void cleanup()
    {
        if (outputFile.exists()) outputFile.delete();
    }
}
