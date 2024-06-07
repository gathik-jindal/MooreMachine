import java.io.FileWriter;
import java.io.IOException;
import java.io.PrintWriter;
import java.util.ArrayList;

import javax.swing.JTextArea;

import java.io.File;

public class GenerateFile 
{
    private PrintWriter pw;

    public GenerateFile(ArrayList<Block> block, JTextArea area)
    {
        try
        {
            pw = new PrintWriter(new FileWriter(new File("main.py")));
        }
        catch(IOException e)
        {
            System.err.println("Cannot edit main.py");
        }

        writeImport();
        writeFunctions(area);
        writeBlock(block);

        pw.close();
    }    

    private void writeImport()
    {
        pw.println("import pydig\n");
        pw.println("pysim = pydig.pydig(name = \"Pydig\")\n");
    }

    private void writeFunctions(JTextArea area)
    {
        pw.println(area.getText() + "\n");
    }

    private void writeBlock(ArrayList<Block> block)
    {
        for(Block b : block)
            pw.println(b);
    }
}
