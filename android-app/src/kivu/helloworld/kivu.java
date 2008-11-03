package kivu.helloworld;

import android.app.Activity;
import android.os.Bundle;
import android.view.View;
import android.widget.AnalogClock;
import android.widget.CheckBox;
public class kivu extends Activity {
    /** Called when the activity is first created. */
    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.main);
        CheckBox cbox = (CheckBox) findViewById(R.id.CheckBox01);
        cbox.setOnClickListener(new View.OnClickListener() {
        	public void onClick(View v) {
        		AnalogClock clock = (AnalogClock) findViewById(R.id.AnalogClock01);
        		clock.setVisibility(((CheckBox)v).isChecked() ? View.VISIBLE : View.INVISIBLE);
        	}
        });
    }
}