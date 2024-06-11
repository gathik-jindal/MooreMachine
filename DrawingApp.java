/**
 * This is the DrawingApp file which allows the user to draw different components. 
 * 
 * @author Aryan, Abhirath, Gathik
 * @version 1.0
 * @since 06/08/2024
 */

import java.awt.CardLayout;
import java.awt.Color;
import java.awt.GridBagConstraints;
import java.awt.GridBagLayout;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;

import javax.swing.JButton;
import javax.swing.JFrame;
import javax.swing.JPanel;

/**
 * The DrawingApp class manages the frame and allows one to run the program.
 */
public class DrawingApp extends JFrame 
{
    private JPanel cards;
    public static final String HOME = "Home", MAIN = "Main";

    /**
     * Creates a Frame and initializes all the panels.
     */
    public DrawingApp() 
    {
        super("Moore Machine Simulator");
        this.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        this.setSize(1500, 800);
        this.setResizable(false);
        
        cards = new JPanel(new CardLayout());

        HomePage home = new HomePage(this);
        cards.add(home, HOME);

        Manager manageMain = new ManageMainCircuit(this);
        cards.add(manageMain, MAIN);

        change(HOME);

        this.getContentPane().add(cards);

        this.setVisible(true);
        this.requestFocusInWindow();
    }

    public void change(String str)
    {
        if(!str.equals(HOME) && !str.equals(MAIN))
            throw new IllegalArgumentException(str + " is not a valid panel type.");
        ((CardLayout)(cards.getLayout())).show(cards, str);
    }

    public static void main(String[] args) 
    {
        new DrawingApp();
    }
}

class HomePage extends JPanel 
{
    private JButton button1;
    private JButton button2;

    public HomePage(DrawingApp frame) 
    {
        setLayout(new GridBagLayout());
        setBackground(Color.ORANGE);
        
        GridBagConstraints gbc = new GridBagConstraints();
        button1 = new JButton("Make a Circuit");
        
        button1.addActionListener(new ActionListener()
        {
            @Override
            public void actionPerformed(ActionEvent e) 
            {
                frame.change(DrawingApp.MAIN);
            }
        });
        
        this.add(button1, gbc);
        this.add(button2, gbc);
    }
}