/**
 * This is the DrawingApp file which allows the user to draw different components. 
 * 
 * @author Aryan, Abhirath, Gathik
 * @version 1.0
 * @since 06/08/2024
 */

import java.awt.CardLayout;

import java.io.IOException;

import javax.swing.JFrame;
import javax.swing.JPanel;

/**
 * The DrawingApp class manages the frame and allows one to run the program.
 */
public class DrawingApp extends JFrame 
{
    private JPanel cards;                           //CardLayout JPanel
    public static final String MAIN = "Main";       //the cards that are in the cardlayout

    /**
     * Creates a Frame and initializes all the panels.
     */
    public DrawingApp() throws IOException
    {
        super("Finite State Machine Simulator");
        this.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        this.setSize(1500, 800);
        this.setResizable(false);
        
        cards = new JPanel(new CardLayout());

        Manager manageMain = new ManageMainCircuit(this);
        cards.add(manageMain, MAIN);

        change(MAIN);

        this.getContentPane().add(cards);

        this.setVisible(true);
        this.requestFocusInWindow();
    }

    /**
     * Changes the panel to the string specified
     * @param str : the new panel
     */
    public void change(String str)
    {
        if(!str.equals(MAIN))
            throw new IllegalArgumentException(str + " is not a valid panel type.");
        ((CardLayout)(cards.getLayout())).show(cards, str);
    }

    public static void main(String[] args) throws IOException
    {
        new DrawingApp();
    }
}