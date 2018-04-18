package mrf.camera2api.testapp;

import android.os.Bundle;
import android.os.Handler;
import android.support.v7.app.AppCompatActivity;

public class Splash extends AppCompatActivity {

    /** Duration of wait **/
    private final int SPLASH_DISPLAY_LENGTH = 3000;

    /** Called when the activity is first created. */
    @Override
    public void onCreate(Bundle icicle) {
        super.onCreate(icicle);
        setContentView(R.layout.activity_splash);
        new Handler().postDelayed(new Runnable() {
            @Override
            public void run() {
                Splash.this.finish();
            }
        }, SPLASH_DISPLAY_LENGTH);
    }
}