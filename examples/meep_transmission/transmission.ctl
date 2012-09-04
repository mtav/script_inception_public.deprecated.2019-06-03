(define-param sx 5) ; size of cell in X direction
;; (define-param sy 32) ; size of cell in Y direction
(set! geometry-lattice (make lattice (size sx no-size no-size)))
(define-param pad 4) ; padding distance between waveguide and cell edge
(define-param w 1) ; width of waveguide
(define-param fcen 1) ; pulse center frequency
(define-param df 2)    ; pulse width (in frequency)
(define-param nfreq 500) ; number of frequencies at which to compute flux
(set-param! resolution 200)
;; (define wvg-ycen (* -0.5 (- sy w (* 2 pad)))) ; y center of horiz. wvg

;wvg-xcen = 0.5*(sx-w-2*pad)
;; (define wvg-xcen (* 0.5 (- sx w (* 2 pad)))) ; x center of vert. wvg
;; (define wvg-xcen 0) ; x center of vert. wvg

(define-param is-reference? false) ; if true, have waveguide, else vaccuum

(if (not is-reference?)
  (set! geometry

	    (list
	    (make block
	      (center 0)
	      (size w infinity infinity)
	      (material (make dielectric (epsilon 12)))))
  )
)

(set! sources (list
               (make source
                 (src (make gaussian-src (frequency fcen) (fwidth df)))
                 (component Ez)
                 (center (+ 1 (* -0.5 sx)) )
                 (size 0 ))))
(set! pml-layers (list (make pml (thickness 1.0))))

(define trans ; transmitted flux
      (add-flux fcen df nfreq
                    (make flux-region
                     (center (- (* 0.5 sx) 1.5) ) (size 0 ))))
(define refl ; reflected flux
      (add-flux fcen df nfreq
                 (make flux-region
                   (center (+ (* -0.5 sx) 1.5) ) (size 0 ))))

(if (not is-reference?) (load-minus-flux "refl-flux" refl))
(run-sources+
  (stop-when-fields-decayed
    50
    Ez
    (vector3 (- (* 0.5 sx) 1.5) )
    1e-3
  )
  (at-beginning output-epsilon)
)
(if is-reference? (save-flux "refl-flux" refl))
(display-fluxes trans refl)

(display "Hello world")(newline)
(display "nfreq = ")(display nfreq)(newline)
(display "sx = ")(display sx)(newline)
;; (display "sy = ")(display sy)(newline)
(display "w = ")(display w)(newline)
(display "fcen = ")(display fcen)(newline)
(display "df = ")(display df)(newline)
(display "resolution = ")(display resolution)(newline)
(display "is-reference? = ")(display is-reference?)(newline)

(exit)
