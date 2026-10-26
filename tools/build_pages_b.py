# -*- coding: utf-8 -*-
"""Remaining service pages + the work index."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pagekit import page, service_ld
from build_pages_a import intro, listing, prose, CTA

# ───────────────────── VIDEOGRAPHER LONDON ─────────────────────
slug = "videographer-london.html"
body = (
  intro("Videographer — London",
        "A London videographer who shoots and edits",
        "One pair of eyes from the first conversation to the final cut. "
        "Based in London, filming across the UK and abroad.")
  + listing("What gets filmed in London", [
      "Corporate &amp; recruitment films",
      "Brand and product work",
      "Events, launches &amp; conferences",
      "Ringside and sport",
      "Property and development",
      "Social cutdowns",
    ])
  + prose("Why one person, not a crew", [
      "Most London production companies sell you a team. That makes sense on a "
      "commercial with a client in the room and a schedule to defend. For most "
      "jobs it means paying for coordination rather than craft.",
      "Here the person who agrees the idea is the person holding the camera and "
      "the person cutting it. Nothing is lost in a handover, because there is no "
      "handover. It is faster, it costs less, and the film ends up closer to what "
      "was discussed.",
      "London work includes ringside coverage for Matchroom Boxing, product film "
      "for WatchTrader &amp; Co and brand work for NOBL.",
    ])
  + CTA.format(H="Tell me about the shoot",
               L="Where, when and what it needs to do. You will get a reply from "
                 "Morgan, not a form response.")
)
n = page(slug,
  "Videographer London | Video Production London — Higher Heights Films",
  "London videographer and video production. Corporate films, brand and product "
  "work, events and sport — directed, shot and edited by one person. Based in "
  "London, filming worldwide.",
  body,
  {"@context": "https://schema.org", "@type": "LocalBusiness",
   "name": "Higher Heights Films", "description":
   "Videographer and video production company based in London.",
   "areaServed": [{"@type": "City", "name": "London"},
                  {"@type": "Country", "name": "United Kingdom"}],
   "url": "https://higher-heights.vercel.app/videographer-london.html"})
print(f"  {slug:36s} {n:,}")

# ───────────────────────── AERIAL ─────────────────────────
slug = "aerial-drone-filming.html"
body = (
  intro("Aerial &amp; drone",
        "Aerial that belongs in the film",
        "Drone work built into the edit rather than bolted on — scale, geography "
        "and movement where the story needs it. UK based, filming worldwide.")
  + listing("Where aerial earns its place", [
      "Property &amp; development",
      "Landscape and location",
      "Automotive tracking",
      "Marine &amp; coastal",
      "Construction progress",
      "Event scale",
    ])
  + prose("A strength, not a separate product", [
      "Aerial is in almost every film made here. That is deliberate — it is not "
      "sold as an add-on with its own line on the invoice, because a drone shot "
      "that exists to justify the drone is obvious to everyone watching.",
      "Used properly it does one of two things: it establishes somewhere so the "
      "viewer knows where they are, or it moves in a way no other camera can. "
      "Anything else is a sunset orbit, and there are enough of those.",
      "Flying is covered and insured for commercial work in the UK.",
    ])
  + CTA.format(H="Tell me about the location",
               L="Where it is and what you need to show. That is enough to come "
                 "back with a plan.")
)
n = page(slug,
  "Aerial &amp; Drone Filming UK | Drone Videographer — Higher Heights Films",
  "UK aerial and drone filming for property, landscape, automotive, marine and "
  "events. Built into the edit rather than sold as an add-on. Commercially "
  "insured, filming worldwide.",
  body,
  service_ld("Aerial and Drone Filming",
             "Aerial and drone filming across the UK for property, landscape, "
             "automotive, marine and events.", slug))
print(f"  {slug:36s} {n:,}")
